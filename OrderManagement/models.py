from django.db import models
from member.models import User,Branchs
from Product.models import Products

# Create your models here.
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
class ShoppingCart(models.Model):
    User=models.ForeignKey(User, on_delete=models.DO_NOTHING,verbose_name="類別")
    Total=models.IntegerField(null=False,verbose_name='總價格')
    class Meta:
        verbose_name = "購物車"
        verbose_name_plural = '購物車'  # 中文名稱
    def __str__(self):
        return self.pk
class ShoppingCartDetails(models.Model):
    Product=models.ForeignKey(Products,on_delete=models.DO_NOTHING,verbose_name='商品')
    Number=models.IntegerField(verbose_name="數量")
    Time=models.DateTimeField(auto_now_add=True)
    Price=models.IntegerField(null=False,verbose_name='價格')
    Total=models.IntegerField(null=False,verbose_name='總價格')
    def __str__(self):
        return self.Product
    class Meta:
        verbose_name = "購物車明細"
        verbose_name_plural = '購物車明細'  # 中文名稱

class Orders(models.Model):
    User=models.ForeignKey(User, on_delete=models.DO_NOTHING,verbose_name="類別")
    Time=models.DateTimeField(auto_now_add=True)
    Delivery_method=models.IntegerField(choices=Delivery_CHOICES,default=1,verbose_name="運送方式",null=True, blank=True)
    Delivery_state=models.IntegerField(choices=State_CHOICES,default=1,verbose_name="運送狀態",null=True, blank=True)
    Payment_method=models.IntegerField(choices=State_CHOICES,default=1,verbose_name="付款方式",null=True, blank=True)
    Payment_time=models.DateTimeField(null=True, blank=True,verbose_name='付款時間')
    Address = models.CharField(max_length=255,verbose_name='地址')
    Total=models.IntegerField(null=False,verbose_name='總價格')
    class Meta:
        verbose_name = "訂單"
        verbose_name_plural = '訂單'  # 中文名稱
    def __str__(self):
        return self.pk
class OrderDetails(models.Model):
    Product=models.ForeignKey(Products,on_delete=models.DO_NOTHING,verbose_name='商品')
    Number=models.IntegerField(verbose_name="數量")
    Price=models.IntegerField(null=False,verbose_name='價格')
    Total=models.IntegerField(null=False,verbose_name='總價格')
    def __str__(self):
        return self.Product
    class Meta:
        verbose_name = "訂單明細"
        verbose_name_plural = '訂單明細'  # 中文名稱

class OrderLog(models.Model):
    Order = models.ForeignKey(Orders, on_delete=models.DO_NOTHING,verbose_name="訂單")
    User=models.ForeignKey(User, on_delete=models.DO_NOTHING,verbose_name="後台操作的員工")
    Time=models.DateTimeField(auto_now_add=True)
    Delivery_state=models.IntegerField(choices=State_CHOICES,default=1,verbose_name="運送狀態",null=True, blank=True)
    class Meta:
        verbose_name = "訂單紀錄"
        verbose_name_plural = '訂單紀錄'  # 中文名稱
    def __str__(self):
        return self.Category_name

