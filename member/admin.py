from django.contrib import admin
from .models import User,Branchs,Transpose
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from Product.models import RestockDetail,Restock

# class RestockDetailInline(admin.TabularInline):  # 或者使用 admin.StackedInline
#     model = RestockDetail
    
#     extra = 1
#     def get_fields(self, request, obj=None):
#         return ['Product', 'Restock', 'ExpiryDate', 'Number', 'Branch']
#     def get_formset(self, request, obj=None, **kwargs):
#         formset = super(RestockDetailInline, self).get_formset(request, obj, **kwargs)
#         if not request.user.is_superuser:
#             for form in formset.form.base_fields:
#                 if form == 'Branch':
#                     formset.form.base_fields[form].disabled = True
#                     formset.form.base_fields[form].initial = request.user.branch
#         return formset
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'user_name','branch', 'phone_number', 'is_active', 'is_staff']
    search_fields = ['email', 'user_name']
    list_filter = ['email', 'user_name']
    ordering = ['email']
    # 定义在添加和更改用户时显示的字段
    fieldsets = (
        ('登入帳號', {'fields': ('phone_number', 'password')}),
        ('使用者資訊', {'fields': ('user_name', 'email', 'birthday', 'bonus_points', 'branch')}),
        ('權限', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('日期相關', {'fields': ('last_login', 'date_joined')}),
    )

    # 定义添加用户时的字段
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2'),
        }),
    )
    # 如果您有自定義的表單，您也可以在這裡設定
    # form = MyUserChangeForm
    # add_form = MyUserCreationForm

    # 如果需要設定自定義的權限管理，您可以在這裡設定
    # filter_horizontal = ()
    # list_filter = ()
    # fieldsets = ()

@admin.register(Branchs)
class BranchsAdmin(admin.ModelAdmin):
    list_display = ['Name','address','phone_number']
    search_fields = ['Name','address','phone_number']
    list_filter = ['Name','address','phone_number']
    ordering = ['Name']

# ['Name','address','phone_number']
@admin.register(Transpose)
class TransposeAdmin(admin.ModelAdmin):
    list_display = ['User','BranchsSend','BranchsReceipt','Time']
    search_fields = ['User','BranchsSend','BranchsReceipt']
    list_filter = ['User','BranchsSend','BranchsReceipt']
    ordering = ['BranchsSend']
    # inlines = [RestockDetailInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super(TransposeAdmin, self).get_form(request, obj, **kwargs)
        if 'User' in form.base_fields:
            form.base_fields['User'].initial = request.user
            form.base_fields['User'].disabled = True
        return form

# ['BranchsSend','BranchsReceipt','Product','Number','Time']