from django.contrib import admin
from .models import Categories,Products,ItemImage,Branch_Inventory,Restock,RestockDetail,RestockDetail_relation
from django.utils.html import format_html
from .forms import RestockForm
# Register your models here.
@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['Category_name','Describe']
    search_fields = ['Category_name','Describe']
    list_filter = ['Category_name','Describe']
    ordering = ['Category_name']
# 'Category_name','Describe'
@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['Category','Item_name', 'Import_price','Price','Specification','Sh']
    search_fields = ['Category','Item_name', 'Import_price','Price','Specification','Sh']
    list_filter = ['Category','Item_name', 'Import_price','Price','Specification','Sh']
    ordering = ['Sh']

# ['Category','Item_name','Price','Specification','Number','Sh']

@admin.register(ItemImage)
class ItemImageAdmin(admin.ModelAdmin):
    list_display = ['ImageID','Products','Image_path']
    search_fields = ['ImageID','Products','Image_path']
    list_filter = ['ImageID','Products','Image_path']
    ordering = ['Products']
    
    def delete_model(self, request, obj):
        # 删除单个对象时的逻辑
        if obj.Image_path:
            obj.Image_path.delete(save=False)
        super(ItemImageAdmin, self).delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        # 删除多个对象时的逻辑
        for obj in queryset:
            if obj.Image_path:
                obj.Image_path.delete(save=False)
        super(ItemImageAdmin, self).delete_queryset(request, queryset)
# ['ImageID','Products','Image_path']
@admin.register(Branch_Inventory)
class Branch_InventoryAdmin(admin.ModelAdmin):
    list_display = ['Products','Number','Branch']
    search_fields = ['Products','Number','Branch']
    list_filter = ['Products','Number','Branch']
    ordering = ['Products']
    def get_form(self, request, obj=None, **kwargs):
        form = super(Branch_InventoryAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['Branch'].disabled = True  
            form.base_fields['Branch'].initial = request.user.branch  

        return form

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.Branch = request.user.branch  
        super(Branch_InventoryAdmin, self).save_model(request, obj, form, change)


# ['Products','ExpiryDate','Number','Branch',]
class RestockDetailInline(admin.TabularInline):  # 或者使用 admin.StackedInline
    model = RestockDetail
    
    extra = 1
    def get_fields(self, request, obj=None):
        return ['Product', 'Restock', 'ExpiryDate', 'Number', 'Branch']
    def get_formset(self, request, obj=None, **kwargs):
        formset = super(RestockDetailInline, self).get_formset(request, obj, **kwargs)
        if not request.user.is_superuser:
            for form in formset.form.base_fields:
                if form == 'Branch':
                    formset.form.base_fields[form].disabled = True
                    formset.form.base_fields[form].initial = request.user.branch
        return formset

@admin.register(Restock)
class RestockAdmin(admin.ModelAdmin):
    # form = RestockForm
    list_display = ['id', 'Category', 'Time', 'Branch', 'User', 'Type', 'content_type', 'object_id','refID']
    # change_form_template = 'admin/restock.html'
    inlines = [RestockDetailInline]
    # class Media:
    #     js = ('js/restock.js',)
    def get_form(self, request, obj=None, **kwargs):
        form = super(RestockAdmin, self).get_form(request, obj, **kwargs)
    #     if not request.user.is_superuser:
        if 'User' in form.base_fields:
            # 自动设置object_id为Branchs的最新ID（或其他逻辑）
            # latest_branch = self.objects.latest('id')
            form.base_fields['Branch'].disabled = True  
            form.base_fields['Branch'].initial = request.user.branch  
            form.base_fields['User'].disabled = True  
            form.base_fields['User'].initial = request.user
            form.base_fields['Category'].disabled = True  
            form.base_fields['Category'].initial = 0
            form.base_fields['content_type'].disabled = True  
            form.base_fields['content_type'].initial = 23
            form.base_fields['object_id'].disabled = True  
            form.base_fields['object_id'].initial = None
        return form
    # def save_model(self, request, obj, form, change):
    #     if not request.user.is_superuser:
    #         obj.Branch = request.user.branch
    #         obj.User = request.user
    
    #     # 确保 object_id 是整数
    #     if form.cleaned_data.get('object_id'):
    #         obj.object_id = form.cleaned_data['object_id']
    #     else:
    #         obj.object_id = None
    #     obj.save()



@admin.register(RestockDetail)
class RestockDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'Product', 'Restock', 'ExpiryDate', 'Number', 'Remain', 'Branch']

@admin.register(RestockDetail_relation)
class RestockDetailRelationAdmin(admin.ModelAdmin):
    list_display = ['id', 'InID', 'OutID', 'Number']