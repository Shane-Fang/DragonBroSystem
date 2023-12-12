from django.contrib import admin
from .models import Categories,Products,ItemImage,Branch_Inventory

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
    list_display = ['Category','Item_name','Price','Specification','Number','Sh']
    search_fields = ['Category','Item_name','Price','Specification','Number','Sh']
    list_filter = ['Category','Item_name','Price','Specification','Number','Sh']
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



# ['Products','ExpiryDate','Number','Branch',]
