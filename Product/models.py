from django.db import models
from django.utils.deconstruct import deconstructible
import os
import time
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.files.storage import default_storage
from member.models import Transpose,Branchs
# from member.models import Branchs

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
    Number=models.IntegerField(verbose_name="總庫存")
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
    Product=models.ForeignKey(Products,on_delete=models.DO_NOTHING,verbose_name='商品')
    Restock=models.ForeignKey(Restock,on_delete=models.CASCADE,verbose_name='交易')
    ExpiryDate=models.DateField(verbose_name='有效日期',null=True, blank=True)
    Number=models.IntegerField(verbose_name="數量")
    Remain=models.IntegerField(null=True, blank=True,verbose_name="剩餘數量")
    Branch=models.ForeignKey('member.Branchs', on_delete=models.DO_NOTHING,verbose_name="分店ID",null=True, blank=True)
    class Meta:
        verbose_name = "進出貨管理明細"
        verbose_name_plural = '進出貨管理明細'  # 中文名稱
    # def __str__(self):
    #     return str(self.Product)
    def save(self, *args, **kwargs):
        # 先存檔RestockDetail資料
        super(RestockDetail, self).save(*args, **kwargs)
        branch_Inventory = Branch_Inventory.objects.filter(Branch=self.Branch,Products=self.Product).first()
        if self.Restock.Category == 0 and (branch_Inventory == None or branch_Inventory.Number == 0): # 第一次匯入csv沒有庫存的邏輯
            inventory = Branch_Inventory.objects.create(  # 
                Products=self.Product, 
                Branch=self.Branch,
                Number=self.Number
            )
            inventory.save()

        elif self.Restock.Category == 0 and branch_Inventory.Number>0: # 進貨且庫存有貨邏輯

            inventory = Branch_Inventory.objects.get(
                Products=self.Product, 
                Branch=self.Branch,
            )
            inventory.Number += self.Number
            inventory.save()

        elif self.Restock.Category == 0 and branch_Inventory.Number<0: # 進貨且庫存欠貨邏輯
            print(f'進貨且庫存欠貨邏輯')
            import_product = RestockDetail.objects.filter(Product=self.Product).order_by('-Remain').first()
            print(f'import product: {import_product}')

        elif self.Restock.Category == 2 and branch_Inventory.Number>0: # 出貨且庫存有貨邏輯
            print(f'出貨且庫存有貨邏輯')
            latest_expiry_restock_detail = RestockDetail.objects.filter(Product=self.Product).order_by('ExpiryDate') # 有效日期排序
            n = self.Number # 暫存出貨number
            Product_total_Remain = branch_Inventory.Number # 暫存inventory number
            for item in latest_expiry_restock_detail:  
                if Restock.objects.get(pk=item.Restock.id).Type == 0: # 只與進貨Restock計算
                    # print(f'item: {item}  Number: {item.Number}  Remain: {item.Remain}  ExDate: {item.ExpiryDate} Restock: {item.Restock.id}')
                    print(f'n: {n} item.Remain {item.Remain} Product total Remain: {Product_total_Remain}')
                    if n > item.Remain: # 出貨number > 進貨remain --> 進貨remain歸零, 進貨remain寫進relation, 出貨number-進貨remain, inventory number-進貨remain
                        print(f'{self} 進貨有效日期:{item.ExpiryDate} 出貨數量:{self.Number} 匹配前進貨remain:{item.Remain} 匹配完進貨remain:{0} relation i o N:{self.id} {item.id} {item.Remain}')
                        Rr = RestockDetail_relation.objects.create(
                            InID=self,
                            OutID=item,
                            Number=item.Remain
                        )
                        n = n - item.Remain
                        Product_total_Remain -= item.Remain
                        item.Remain = 0
                        item.save()

                    if n <= item.Remain: # 出貨number < 進貨remain --> 出貨number寫進relation, 進貨remain-出貨number, inventory number-出貨number
                        print(f'{self} 進貨有效日期:{item.ExpiryDate} 出貨數量:{self.Number} 匹配前進貨remain:{item.Remain} 匹配完進貨remain:{item.Remain-n}')
                        Rr = RestockDetail_relation.objects.create(
                            InID=self,
                            OutID=item,
                            Number=n
                        )
                        item.Remain = item.Remain-n
                        item.save()
                        Product_total_Remain = Product_total_Remain-n
                        n=0
                        break

            if n > 0: # 出貨遍歷完進貨number仍有貨 --> 找最新的進貨有效日期並將remain - 剩餘的進貨number
                print(f'{self} 進貨有效日期:{item.ExpiryDate} 出貨數量:{self.Number} 匹配前進貨remain:{item.Remain} 匹配完進貨remain:{-n}')
                item = latest_expiry_restock_detail.last()
                item.Remain = -n
                item.save()
                Product_total_Remain = -n

            inventory = Branch_Inventory.objects.get(
                Products=self.Product, 
                Branch=self.Branch,
            )
            inventory.Number = Product_total_Remain
            inventory.save()

        elif self.Restock.Category == 2 and branch_Inventory.Number<=0: # 出貨且庫存沒貨邏輯
            print(f'出貨且庫存沒貨邏輯')
            latest_expiry_restock_detail = RestockDetail.objects.filter(Product=self.Product).order_by('ExpiryDate') # 有效日期排序
            item = latest_expiry_restock_detail.last()
            print(f'{self} 進貨有效日期:{item.ExpiryDate} 出貨數量:{self.Number} 匹配前進貨remain:{item.Remain}')
            item.Remain = item.Remain - self.Number
            item.save()
            print(f'{branch_Inventory.Products} 分店:{branch_Inventory.Branch} 出貨數量:{self.Number} 匹配完進貨remain:{item.Remain}')
            
            inventory = Branch_Inventory.objects.get(
                Products=self.Product, 
                Branch=self.Branch,
            )
            inventory.Number = inventory.Number - self.Number
            inventory.save()
            
            print(f'{self} 進貨有效日期:{item.ExpiryDate} 出貨數量:{self.Number} 匹配完進貨remain:{item.Remain}')


        # if self.Restock.Type == 0 and branch_Inventory.Number<=0:
        #     latest_expiry_restock_detail = RestockDetail.objects.filter(Product=self.Product).order_by('-ExpiryDate').first()
        #     if latest_expiry_restock_detail:
        #         restocks = Restock.objects.filter(Type=1)
        #         restock_detail_ids = RestockDetail.objects.filter(Restock__in=restocks).order_by('-pk').first()
        #         if self.Number>restock_detail_ids.Number:
        #             number=restock_detail_ids.Number
        #         elif self.Number<restock_detail_ids.Number:
        #             number=self.Number
        #         inventory = RestockDetail_relation(
        #             InID=self.pk,
        #             OutID=restock_detail_ids.pk,
        #             Number=number
        #         )
        #         inventory.save()

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