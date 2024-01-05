import datetime
from io import TextIOWrapper
import os
from django.conf import settings
from django.contrib import admin
import pandas as pd
from .models import Categories,Products,ItemImage,Branch_Inventory,Restock,RestockDetail,RestockDetail_relation
from member.models import User, Branchs
from django.utils.html import format_html
from .forms import RestockForm
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from django import forms
from django.urls import path
from django.shortcuts import redirect, render
import csv
from django.core.files.storage import FileSystemStorage

def import_csv_data(file_path, user_id, branch_id):
        
        with open(file_path, 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            print(f'csv: {file_path}, user id: {user_id}, branch id: {branch_id}')
            restock = Restock.objects.create(
                Time=datetime.datetime.now(),  # 使用当前时间
                Category=0,  # 固定上架类别
                Branch_id=branch_id,
                User_id=user_id
            )
            for row in reader:
                print(row)
                if row['Item_name'] != '':
                    Item_name = row['Item_name']
                    number = int(row['Number'])
                    expiry_date = pd.Timestamp(row['ExpiryDate']).date()  # 假设日期格式为'YYYY-MM-DD'

                    # 查找或创建产品记录
                    product, created = Products.objects.get_or_create(Item_name=Item_name)

                    print(f'product id: {product.id}, restock id: {restock.id}')

                    # 创建RestockDetail记录
                    RestockDetail.objects.create(
                        ExpiryDate=expiry_date,
                        Number=number,
                        Remain=number,
                        Product_id=product.id,
                        Restock_id=restock.id,
                        Branch_id=branch_id
                    )

                    # 查找或创建Branch_Inventory记录
                    branch_inventory, _ = Branch_Inventory.objects.get_or_create(Branch_id=branch_id, Products_id=product.id)
                    branch_inventory.save()
class CategoriesResource(resources.ModelResource):
    class Meta:
        model = Categories
        exclude = ('id',)
        skip_unchanged = True
        report_skipped = True
        fields = ('Category_name', 'Describe',)
        import_id_fields = ("Category_name",)

class ProductsResource(resources.ModelResource):
    Category  = fields.Field(
        column_name='Category_name',
        attribute='Category',
        widget=ForeignKeyWidget(Categories, 'Category_name')
    )
    class Meta:
        model = Products
        exclude = ('id',)
        fields = ('Category_name', 'Item_name', 'Price', 'Import_price', 'Specification', 'Sh')
        import_id_fields = ("Item_name",)


class RestockResource(resources.ModelResource):
    product_name = fields.Field(
        column_name='product_name',
        attribute='Product',
        widget=ForeignKeyWidget(Products, 'product_name')
    )

    user_id = fields.Field(
        column_name='user_id',
        attribute='User',
        widget=ForeignKeyWidget(User, 'id')
    )

    branch_id = fields.Field(
        column_name='branch_id',
        attribute='Brunchs',
        widget=ForeignKeyWidget(Branchs, 'id')
    )
    
    class Meta:
        model = RestockDetail
        import_id_fields = ('id',)
        fields = ('Item_name', 'ExpiryDate', 'Number')
        import_id_fields = ("Item_name",)

class ItemImageDetailInline(admin.TabularInline):  # 或者使用 admin.StackedInline
    model = ItemImage
    extra = 1
    def get_fields(self, request, obj=None):
        return ['ImageID', 'Products', 'Image_path']
# Register your models here.
@admin.register(Categories)
class CategoriesAdmin(ImportExportModelAdmin):
    resource_class=CategoriesResource
    list_display = ['Category_name','Describe']
    search_fields = ['Category_name','Describe']
    list_filter = ['Category_name','Describe']
    ordering = ['Category_name']
# 'Category_name','Describe'
@admin.register(Products)
class ProductsAdmin(ImportExportModelAdmin):
    resource_class=ProductsResource
    list_display = ['Category','Item_name', 'Import_price','Price','Specification','Sh']
    search_fields = ['Item_name']
    list_filter = ['Category','Item_name', 'Import_price','Price','Specification','Sh']
    ordering = ['Sh']
    inlines=[ItemImageDetailInline]

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
        for form in formset.form.base_fields:
            if form == 'Branch':
                formset.form.base_fields[form].disabled = True
                formset.form.base_fields[form].initial = request.user.branch
        return formset


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()

@admin.register(Restock)
class RestockAdmin(admin.ModelAdmin):
    change_list_template = "admin/Restock_changelist.html"
    form = RestockForm
    list_display = ['id', 'Category', 'Time', 'Branch', 'User', 'Type', 'content_type', 'object_id']
    # change_form_template = 'admin/restock.html'
    inlines = [RestockDetailInline]
    class Media:
        js = ('js/restock.js',)
    def get_form(self, request, obj=None, **kwargs):
        form = super(RestockAdmin, self).get_form(request, obj, **kwargs)
        if 'User' in form.base_fields:
            form.base_fields['Branch'].disabled = True  
            form.base_fields['Branch'].initial = request.user.branch  
            form.base_fields['User'].disabled = True  
            form.base_fields['User'].initial = request.user
            form.base_fields['Category'].widget = forms.Select(choices=[
                (0, '進貨'),
                (1, 'BtoB'),
            ])

        return form

    
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        user_id = request.user.id
        branch_id = User.objects.get(id=user_id).branch_id

        if request.method == "POST":
            csv_file = request.FILES["csv_file"]

            fs = FileSystemStorage(location=os.path.join(settings.CSV_ROOT, 'restock'))
            filename = fs.save(csv_file.name, csv_file)
            file_path = fs.path(filename)

            import_csv_data(file_path, user_id, branch_id)
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        csvform = CSVImportForm()
        payload = {"form": csvform}
        return render(request, "admin/csv_form.html", payload)

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