from django.contrib import admin
from .models import User,Branchs,Transpose

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'user_name', 'phone_number', 'is_active', 'is_staff']
    search_fields = ['email', 'user_name']
    ordering = ['email']
    # 如果您有自定義的表單，您也可以在這裡設定
    # form = MyUserChangeForm
    # add_form = MyUserCreationForm

    # 如果需要設定自定義的權限管理，您可以在這裡設定
    # filter_horizontal = ()
    # list_filter = ()
    # fieldsets = ()

@admin.register(Branchs)
class BranchsAdmin(admin.ModelAdmin):
    list_display = ['Name']
    search_fields = ['Name']
    ordering = ['Name']

@admin.register(Transpose)
class TransposeAdmin(admin.ModelAdmin):
    list_display = ['BranchsSend','BranchsReceipt','Product','Number','Time']
    search_fields = ['BranchsSend','BranchsReceipt','Product']
    ordering = ['BranchsSend']

# ['BranchsSend','BranchsReceipt','Product','Number','Time']