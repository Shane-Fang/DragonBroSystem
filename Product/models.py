from datetime import datetime
from django.db import models
from django.utils.deconstruct import deconstructible
import os
import time
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.files.storage import default_storage
from member.models import Transpose,Branchs
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import uuid
from django.db import models, connection

# from member.models import Branchs

def gen_RestockDetail_id():
    now = datetime.now()
    # 将日期时间转换为ISO格式字符串，去掉连字符和冒号，并附加UUID的前12个字符
    return f"{now.strftime('%Y%m%d%H%M%S%f')}{uuid.uuid4().hex}"

State_CHOICES = (
        (0, '代處理'),
        (1, '已處理'),
    )
Delivery_CHOICES = (
        (0, '自取'),
        (1, '寄送'),
    )
Payment_CHOICES = (
        (0, '親自付款'),
        (1, '貨到付款'),
    )
@deconstructible
class UploadToPathAndRename(object):
    def __init__(self, path):
        self.sub_path = path
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # 使用 ImageID 作为文件名（如果已经生成）
        if instance.ImageID:
            filename = f'{instance.ImageID}.{ext}'
        else:
            # 如果 ImageID 还未生成，则使用默认名称或其他逻辑
            filename = f'default.{ext}'

        # 构造文件路径
        return os.path.join(self.sub_path, filename)
# Create your models here.
class Categories(models.Model):
    Category_name=models.CharField(max_length=99,verbose_name="類別名稱")
    Describe=models.CharField(max_length=99,verbose_name="類別描述")
    class Meta:
        verbose_name = "類別管理"
        verbose_name_plural = '類別管理'  # 中文名稱
    def __str__(self):
        return self.Category_name



class Products(models.Model):
    Sh_CHOICES = (
        (0, '下架'),
        (1, '上架'),
    )
    Category=models.ForeignKey(Categories, on_delete=models.CASCADE,verbose_name="類別",null=True, blank=True)
    Item_name=models.CharField(max_length=99,verbose_name="貨品名稱",null=True, blank=True)
    Price=models.IntegerField(verbose_name="建議售價")
    Import_price=models.IntegerField(verbose_name="成本價")
    Specification=models.CharField(max_length=99,verbose_name="規格",null=True, blank=True)
    Sh=models.IntegerField(choices=Sh_CHOICES,default=1,verbose_name="上/下架")
    # def save(self, *args, **kwargs):
    #     try:
    #         # is there an instance already in the database?
    #         obj = ProductModel.objects.get(pk=self.pk)
    #         # an object was found with this id, check if the path is different
    #         if obj.Product_images and self.Product_images and obj.Product_images.path != self.Product_images.path:
    #             # path is different, delete the old file from the storage
    #             default_storage.delete(obj.Product_images.path)
    #     except ProductModel.DoesNotExist:
    #         # Object is new, so field hasn't technically changed, but you may want to do something else here
    #         pass
        
    #     # Call the "real" save() method.
    #     super(ProductModel, self).save(*args, **kwargs)
    class Meta:
        verbose_name = "商品管理"
        verbose_name_plural = '商品管理'  # 中文名稱
    def __str__(self):
        return str(self.Item_name)

class Branch_Inventory(models.Model):
    Products=models.ForeignKey(Products,on_delete=models.DO_NOTHING,verbose_name='商品',related_name='inventory_records')
    Number=models.IntegerField(verbose_name="總庫存",default=0)
    Branch=models.ForeignKey('member.Branchs',on_delete=models.DO_NOTHING,verbose_name='店家')
    class Meta:
        verbose_name = "分店商品庫存"
        verbose_name_plural = '分店商品庫存'  # 中文名稱
    def __str__(self):
        return str(self.Products)



class ItemImage(models.Model):
    ImageID=models.AutoField(auto_created = True,primary_key=True,verbose_name='圖片id')
    Products=models.ForeignKey(Products,on_delete=models.DO_NOTHING,verbose_name='商品')
    Image_path= models.ImageField(
        upload_to=UploadToPathAndRename('image/productimage/'),
        blank=False,
        null=False,
        verbose_name="商品圖片"
    )
    class Meta:
        verbose_name = "圖片管理"
        verbose_name_plural = '圖片管理'  # 中文名稱
    def __str__(self):
        return str(self.ImageID)
    def save(self, *args, **kwargs):
        # 检查是否已经有文件被上传
        if self.Image_path and not hasattr(self, '_temp_image_path'):
            # 临时保存原始文件
            self._temp_image_path = self.Image_path

        # 首先保存模型，但不包括文件字段
        self.Image_path = None
        super(ItemImage, self).save(*args, **kwargs)

        # 如果有临时文件，恢复它
        if hasattr(self, '_temp_image_path'):
            self.Image_path = self._temp_image_path
            del self._temp_image_path

        # 现在 ImageID 已经生成，可以再次保存模型，包括文件字段
        super(ItemImage, self).save(*args, **kwargs)
    

    def delete(self, *args, **kwargs):
        # 打印文件路径，确认是否正确
        if self.Image_path:
            # 尝试删除文件
            try:
                self.Image_path.delete(save=False)
                print(f"File {self.Image_path.path} deleted")
            except Exception as e:
                print(f"Error deleting file: {e}")

        super(ItemImage, self).delete(*args, **kwargs)

class Restock(models.Model):
    Category_CHOICES=((0,'進貨'),
                    (1,'BtoB'),
                    (2,'BtoC'),
                    )
    Type_CHOICES=(
        (0,'進貨'),
        (1,'出貨'),
    )
    Category=models.IntegerField(choices=Category_CHOICES,default=0,verbose_name="進貨狀態",null=True, blank=True)
    Time=models.DateTimeField(auto_now_add=True)
    Branch=models.ForeignKey('member.Branchs', on_delete=models.DO_NOTHING,verbose_name="分店ID")
    User=models.ForeignKey('member.User', on_delete=models.DO_NOTHING,verbose_name="後台操作的員工")
    Type=models.IntegerField(choices=Type_CHOICES,default=1,verbose_name="進出貨",null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,null=True, blank=True,verbose_name="分店/訂單")
    object_id = models.PositiveIntegerField(null=True, blank=True,verbose_name="分店/訂單的ID")
    refID = GenericForeignKey('content_type', 'object_id') # 主要是連結Order or Transpose
    class Meta:
        verbose_name = "進出貨管理"
        verbose_name_plural = '進出貨管理'  # 中文名稱
    def save(self, *args, **kwargs):
        # 先存檔RestockDetail資料
        super(Restock, self).save(*args, **kwargs)
        if self.Category == 1:
            # 創建或更新Branch_Inventory資料表
            Receipt = Branchs.objects.get(id=self.object_id)
            inventory, created = Transpose.objects.get_or_create(
                BranchsSend=self.Branch,
                BranchsReceipt=Receipt,
                User=self.User,
            )
            inventory.save()

class RestockDetail(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    Product=models.ForeignKey(Products,on_delete=models.DO_NOTHING,verbose_name='商品')
    Restock=models.ForeignKey(Restock,on_delete=models.CASCADE,verbose_name='交易')
    ExpiryDate=models.DateField(verbose_name='有效日期',null=True, blank=True)
    Number=models.IntegerField(verbose_name="數量")
    Remain=models.IntegerField(null=True, blank=True,verbose_name="剩餘數量")
    Branch=models.ForeignKey('member.Branchs', on_delete=models.DO_NOTHING,verbose_name="分店ID",null=True, blank=True)
    class Meta:
        verbose_name = "進出貨管理明細"
        verbose_name_plural = '進出貨管理明細'  # 中文名稱
    def __str__(self):
        return str(self.Product)
    
    def save(self, *args, **kwargs):
        
        if not self.pk:
            self.pk = uuid.uuid4()
        temp_Rr = []
        branch_Inventory, created = Branch_Inventory.objects.get_or_create(Branch=self.Branch, Products=self.Product)

        if self.Restock.Category == 0 and branch_Inventory.Number<0: # 進貨且庫存欠貨邏輯
            print(f'進貨且庫存欠貨邏輯')
            RD = RestockDetail.objects.filter(
                Remain__lt=0,  
                Restock__Type=1,  
                Product=self.Product  
            ).order_by('Restock__Time')
            n = self.Remain # 暫存進貨Remain
            for item in RD:
                if Restock.objects.get(pk=item.Restock.id).Type == 1: # 只與出貨Restock計算
                    
                    if n > -(item.Remain):
                        print('進貨remain > 出貨remain')
                        print(f'{self} 進貨有效日期:{self.ExpiryDate} 匹配前進貨remain:{self.Remain} 匹配前出貨remain:{item.Remain} {item}')
                        
                        temp_Rr.append({'OutID': item, 'Number': -(item.Remain)})
                        # RestockDetail_relation.insert_restock_detail_relation(self.id, item.id, -(item.Remain))
                        print(f'{self} 進貨有效日期:{self.ExpiryDate} 匹配後進貨remain:{self.Remain} 匹配後出貨remain:{item.Remain} relation i o N:{self.id} {item.id} {-(item.Remain)}')
                        n = n + item.Remain
                        item.Remain = 0
                        item.save()
                        self.Remain = n
                        

                    elif n < -(item.Remain):
                        print('進貨remain < 出貨remain')
                        print(f'{self} 進貨有效日期:{self.ExpiryDate} 匹配前進貨remain:{self.Remain} 匹配前出貨remain:{item.Remain}')
                        
                        temp_Rr.append({'OutID': item, 'Number': self.Remain})
                        # RestockDetail_relation.insert_restock_detail_relation(self.id, item.id, self.Remain)
                        print(f'{self} 進貨有效日期:{self.ExpiryDate} 匹配前進貨remain:{self.Remain} 匹配前出貨remain:{item.Remain} relation i o N:{self.id} {item.id} {self.Remain}')
                        item.Remain = item.Remain + self.Remain
                        item.save()
                        n = 0
                        self.Remain = n
                        break

        elif self.Restock.Category == 2 and branch_Inventory.Number>0: # 出貨且庫存有貨邏輯
            print(f'出貨且庫存有貨邏輯')
            latest_expiry_restock_detail = RestockDetail.objects.filter(Product=self.Product, Remain__gt=0).order_by('ExpiryDate') # 有效日期排序
            n = self.Number # 暫存出貨number
            for item in latest_expiry_restock_detail:  
                if Restock.objects.get(pk=item.Restock.id).Type == 0: # 只與進貨Restock計算
                    # print(f'item: {item}  Number: {item.Number}  Remain: {item.Remain}  ExDate: {item.ExpiryDate} Restock: {item.Restock.id}')
                    print(f'n: {n} item.Remain {item.Remain}')
                    if n > item.Remain: # 出貨number > 進貨remain --> 進貨remain歸零, 進貨remain寫進relation, 出貨number-進貨remain, inventory number-進貨remain
                        print('出貨number > 進貨remain')
                        print(f'出貨數量:{self.Number} 匹配前出貨remain:{self.Remain} 進貨有效日期:{item.ExpiryDate} 匹配前進貨remain:{item.Remain} relation i o N:{item.id} {self.id} {item.Remain}')
                        Rr = RestockDetail_relation.objects.create(
                            InID=item,
                            OutID=self,
                            Number=item.Remain
                        )
                        self.Remain = self.Remain + item.Remain
                        n = n - item.Remain
                        item.Remain = 0
                        item.save()
                        print(f'出貨數量:{self.Number} 匹配後出貨remain:{self.Remain} 進貨有效日期:{item.ExpiryDate} 匹配後進貨remain:{item.Remain} relation i o N:{item.id} {self.id} {item.Remain}')

                    if n <= item.Remain: # 出貨number < 進貨remain --> 出貨number寫進relation, 進貨remain-出貨number, inventory number-出貨number
                        print('出貨number < 進貨remain')
                        print(f'出貨數量:{self.Number} 匹配前出貨remain:{self.Remain} 進貨有效日期:{item.ExpiryDate} 匹配前進貨remain:{item.Remain} relation i o N:{item.id} {self.id} {item.Remain}')
                        Rr = RestockDetail_relation.objects.create(
                            InID=item,
                            OutID=self,
                            Number=n
                        )
                        item.Remain = item.Remain-n
                        item.save()
                        n=0
                        self.Remain = n
                        
                        print(f'出貨數量:{self.Number} 匹配後出貨remain:{self.Remain} 進貨有效日期:{item.ExpiryDate} 匹配後進貨remain:{item.Remain} relation i o N:{item.id} {self.id} {item.Remain}')

                        break
        
        # 先存檔RestockDetail資料
        super(RestockDetail, self).save(*args, **kwargs)
        if self.Restock.Category == 0:
            for item in temp_Rr:
                Rr = RestockDetail_relation.objects.create(
                            InID=self,
                            OutID=item['OutID'],
                            Number=item['Number']
                        )


class RestockDetail_relation(models.Model):
    InID=models.ForeignKey(RestockDetail,on_delete=models.DO_NOTHING,verbose_name='InID',related_name='InID')
    OutID=models.ForeignKey(RestockDetail,on_delete=models.DO_NOTHING,verbose_name='OutID',related_name='OutID')
    Number=models.IntegerField(verbose_name="數量")
    class Meta:
        verbose_name = "進出貨管理明細管理"
        verbose_name_plural = '進出貨管理明細管理'  # 中文名稱
    # def __str__(self):
    #     return self.Category_name
    def save(self, *args, **kwargs):
        super(RestockDetail_relation, self).save(*args, **kwargs)

    def insert_restock_detail_relation(InID_id, OutID_id, Number):
        print(str(InID_id))
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Product_RestockDetail_relation (InID_id, OutID_id, Number) VALUES (%s, %s, %s)",
                [str(InID_id), str(OutID_id), Number]
            )

@receiver([post_save, post_delete], sender=RestockDetail)
def update_branch_inventory(sender, instance, **kwargs):
    branch_id = instance.Branch
    product_id = instance.Product
    remain_sum = RestockDetail.objects.filter(Branch=branch_id,Product=product_id).aggregate(total_remain=models.Sum('Remain'))['total_remain']
    if remain_sum is not None:
        inventory, created = Branch_Inventory.objects.get_or_create(Branch=branch_id, Products=product_id)
        inventory.Number = remain_sum
        inventory.save()
    else:
        # 如果没有 RestockDetail 则将 Branch_Inventory 删除
        Branch_Inventory.objects.filter(Branch=branch_id, Products=product_id).delete()

@receiver(post_save, sender=RestockDetail)
def update_remain(sender, instance, created, **kwargs):
    if created:
        # 执行您的操作，访问 instance.id 和 instance.Remain 属性
        print(f'RestockDetail id: {instance.id}, Remain: {instance.Remain}')