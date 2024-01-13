from django.db import models
from member.models import User,Branchs
from Product.models import Products,Branch_Inventory,Restock,ContentType
from django.db.models import Sum
from django.core.exceptions import ValidationError
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
    branch = models.ForeignKey(Branchs,on_delete=models.DO_NOTHING,verbose_name='店家',null=True, blank=True)
    class Meta:
        verbose_name = "購物車"
        verbose_name_plural = '購物車'  #
    def __str__(self):
        return str(self.pk)
class ShoppingCartDetails(models.Model):
    Products=models.ForeignKey(Products,on_delete=models.DO_NOTHING,verbose_name='商品')
    ShoppingCart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='details', verbose_name='購物車')
    Number=models.IntegerField(null=True, blank=True,verbose_name="數量")
    Time=models.DateTimeField(auto_now_add=True)
    Price=models.IntegerField(null=True,verbose_name='價格')
    Total=models.IntegerField(null=True,verbose_name='總價格')
    def __str__(self):
        return str(self.Products)
    def save(self, *args, **kwargs):
        # 先存ShoppingCartDetails
        super(ShoppingCartDetails, self).save(*args, **kwargs)

        # 後更新ShoppingCart價格
        total = self.ShoppingCart.details.aggregate(Sum('Total'))['Total__sum'] or 0
        self.ShoppingCart.Total = total
        self.ShoppingCart.save()
    def delete(self, *args, **kwargs):
        cart = self.ShoppingCart  # 保存关联的购物车
        super(ShoppingCartDetails, self).delete(*args, **kwargs)  
        
        total = cart.details.aggregate(Sum('Total'))['Total__sum'] or 0
        cart.Total = total
        cart.save()
        if total == 0:
            cart.delete()
    class Meta:
        verbose_name = "購物車明細"
        verbose_name_plural = '購物車明細'  # 中文名稱

class Orders(models.Model):
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
    User=models.ForeignKey(User, on_delete=models.DO_NOTHING,verbose_name="類別")
    branch = models.ForeignKey(Branchs,on_delete=models.DO_NOTHING,verbose_name='店家',null=True, blank=True)
    Time=models.DateTimeField(auto_now_add=True)
    Delivery_method=models.IntegerField(choices=Delivery_CHOICES,default=1,verbose_name="運送方式",null=True, blank=True)
    Delivery_state=models.IntegerField(choices=State_CHOICES,default=1,verbose_name="運送狀態",null=True, blank=True)
    Payment_method=models.IntegerField(choices=Payment_CHOICES,default=1,verbose_name="付款方式",null=True, blank=True)
    Payment_time=models.DateTimeField(null=True, blank=True,verbose_name='付款時間')
    Address = models.CharField(max_length=255,verbose_name='地址')
    Total=models.IntegerField(null=False,verbose_name='總價格')
    class Meta:
        verbose_name = "訂單"
        verbose_name_plural = '訂單'
    def __str__(self):
        return str(self.pk)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        OrderLog.objects.create(
            Order=self,
            User=self.User, 
            Delivery_state=self.Delivery_state
        )
        content_type_obj = ContentType.objects.get(id=16)
        Restock.objects.create(
            Category=2,
            Branch=self.branch,
            User=self.User, 
            Type=1,
            content_type=content_type_obj,
            object_id=self.id
        )

class OrderDetails(models.Model):
    Order = models.ForeignKey(Orders, on_delete=models.CASCADE,verbose_name='訂單編號')
    Products=models.ForeignKey(Products,on_delete=models.DO_NOTHING,verbose_name='商品')
    Number=models.IntegerField(verbose_name="數量")
    Price=models.IntegerField(null=False,verbose_name='價格')
    Total=models.IntegerField(null=False,verbose_name='總價格')
    def __str__(self):
        return str(self.pk)
    class Meta:
        verbose_name = "訂單明細"
        verbose_name_plural = '訂單明細'  
    def save(self, *args, **kwargs):
        if not self.pk or 'Number' in kwargs.get('update_fields', []):
            branch_inventory = Branch_Inventory.objects.filter(Products=self.Products,Branch=self.Order.branch).first()
            if branch_inventory: 
                new_quantity = branch_inventory.Number - self.Number
                # if new_quantity < 0:
                #     print("庫存不足，無法完成訂單")
                #     raise ValidationError("庫存不足，無法完成訂單")
                # else:
                branch_inventory.Number = new_quantity
                branch_inventory.save()
            else:
                raise ValidationError("找不到相關的庫存記錄")
        super().save(*args, **kwargs)


class OrderLog(models.Model):
    Order = models.ForeignKey(Orders, on_delete=models.DO_NOTHING,verbose_name="訂單")
    User=models.ForeignKey(User, on_delete=models.DO_NOTHING,verbose_name="後台操作的員工")
    Time=models.DateTimeField(auto_now_add=True)
    Delivery_state=models.IntegerField(choices=State_CHOICES,default=1,verbose_name="運送狀態",null=True, blank=True)
    class Meta:
        verbose_name = "訂單紀錄"
        verbose_name_plural = '訂單紀錄'  # 中文名稱
    # def __str__(self):
    #     return self.Time

