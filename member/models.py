from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from Product.models import Products


class Branchs(models.Model):
    Name=models.CharField(max_length=15,verbose_name='店家名稱')
    address = models.CharField(max_length=255,verbose_name='店家地址')
    phone_number = models.CharField(max_length=15,verbose_name='店家電話')
    def __str__(self):
        return self.Name
    class Meta:
        verbose_name = "店家"
        verbose_name_plural = '店家'  # 中文名稱
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True,verbose_name='信箱')
    user_name = models.CharField(max_length=150,verbose_name='姓名')
    phone_number = models.CharField(max_length=15,verbose_name='電話')
    birthday = models.DateField(null=True, blank=True,verbose_name='生日')
    address = models.CharField(max_length=255,verbose_name='地址')
    bonus_points = models.IntegerField(default=0,verbose_name='點數')
    branch = models.ForeignKey(Branchs,on_delete=models.DO_NOTHING,verbose_name='店家',null=True, blank=True)
    # 以下是 AbstractBaseUser 已經提供的欄位
    # password 字段由 AbstractBaseUser 自動處理
    # last_login 也是由 AbstractBaseUser 提供
    is_active = models.BooleanField(default=True,verbose_name='啟動帳戶')
    is_staff = models.BooleanField(default=False,verbose_name='訪問後台權限')
    date_joined = models.DateTimeField(default=timezone.now,verbose_name='最後登入')
    objects = UserManager()
    USERNAME_FIELD = 'email'    #登入帳號的欄位
    REQUIRED_FIELDS = ['user_name']     #非必要填寫欄位


    def __str__(self):
        return self.email
    class Meta:
        verbose_name = "帳號"
        verbose_name_plural = '帳號'  # 中文名稱
    # 這裡可以添加任何自定義方法，例如積分方法或其他業務邏輯


class Transpose(models.Model):
    BranchsSend=models.ForeignKey(Branchs,on_delete=models.DO_NOTHING,verbose_name='寄送方', related_name='send_transposes')
    BranchsReceipt=models.ForeignKey(Branchs,on_delete=models.DO_NOTHING,verbose_name='收獲方', related_name='receipt_transposes')
    Product=models.ForeignKey(Products,on_delete=models.DO_NOTHING,verbose_name='商品')
    Number=models.IntegerField(verbose_name="數量")
    Time=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "運送"
        verbose_name_plural = '運送'  # 中文名稱
    def __str__(self):
        return self.BranchsSend + self.BranchsReceipt 



