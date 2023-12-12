from django.db import models
from django.utils.deconstruct import deconstructible
import os
import time
from django.core.files.storage import default_storage
# from member.models import Branchs
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
    Specification=models.CharField(max_length=99,verbose_name="規格")
    Number=models.IntegerField(verbose_name="庫存",)
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
        return self.Item_name

class Branch_Inventory(models.Model):
    Products=models.ForeignKey(Products,on_delete=models.DO_NOTHING,verbose_name='商品')
    Number=models.IntegerField(verbose_name="總庫存")
    Branch=models.ForeignKey('member.Branchs',on_delete=models.DO_NOTHING,verbose_name='店家')
    class Meta:
        verbose_name = "進貨商品管理"
        verbose_name_plural = '進貨商品管理'  # 中文名稱
    def __str__(self):
        return self.Products



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
        print(f"Deleting file: {self.Image_path.path}")

        if self.Image_path:
            # 尝试删除文件
            try:
                self.Image_path.delete(save=False)
                print(f"File {self.Image_path.path} deleted")
            except Exception as e:
                print(f"Error deleting file: {e}")

        super(ItemImage, self).delete(*args, **kwargs)

