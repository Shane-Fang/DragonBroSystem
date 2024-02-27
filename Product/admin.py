import datetime
from io import TextIOWrapper
import os
from django.conf import settings
from django.contrib import admin
import pandas as pd
from .models import Categories,Products,ItemImage,Branch_Inventory,Restock,RestockDetail,RestockDetail_relation, Transpose
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
        
    if 'xlsx' in file_path:
        data = pd.read_excel(file_path)
    elif 'csv' in file_path:
        data = pd.read_csv(file_path)
    else:
        data = pd.read_table(file_path)

    restock = Restock.objects.create(
            Time=datetime.datetime.now(),  # 使用当前时间
            Category=0,  # 固定上架类别
            Branch_id=branch_id,
            User_id=user_id,
            Type=0,
        )
    
    for index, row in data.iterrows():
        if row['名稱'] != '' or not pd.isna(row['名稱']):
            Item_Category = row['類別']
            Item_name = row['名稱']
            price = int(row['銷售價格'])
            import_price = int(row['入貨成本'])
            number = int(row['數量'])

            if pd.isna(row['有效日期']):
                expiry_date = None  # 如果是 NaT，則將日期設為 None
            else:
                expiry_date = pd.Timestamp(row['有效日期']).date()

            product = Products.objects.get(Item_name=Item_name)

            # print(product.Item_name)

            RestockDetail.objects.create(
                    ExpiryDate=expiry_date,
                    Number=number,
                    Remain=number,
                    Product_id=product.pk,
                    Restock_id=restock.pk,
                    Import_price=import_price,
                    Branch_id=branch_id
                )

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
        fields = ('Category_name', 'Item_name', 'Price',  'Specification', 'Sh')
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
    list_display = ['Category','Item_name', 'Price','Specification','Sh']
    search_fields = ['Item_name']
    list_filter = ['Category','Item_name', 'Price','Specification','Sh']
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
    list_display = ['Products','Number','Branch','display_inventory_status']
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
    def display_inventory_status(self, obj):

        return "現貨" if obj.Number >= 0 else "預售"
    display_inventory_status.short_description = "庫存狀態" 
    display_inventory_status.admin_order_field = 'Number'


# ['Products','ExpiryDate','Number','Branch',]
class RestockDetailInline(admin.TabularInline):  # 或者使用 admin.StackedInline
    model = RestockDetail
    extra = 1
    def get_fields(self, request, obj=None):
        return ['Product', 'Restock', 'ExpiryDate', 'Number', 'Branch', 'Import_price']
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
    list_display = ['id', 'Category', 'Time', 'Branch', 'User', 'Type', 'content_type', 'object_id','refID']
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

            now = datetime.datetime.now()
            date_time = now.strftime("%Y%m%d_%H%M%S")

            # 取得原始檔案副檔名
            _, file_extension = os.path.splitext(csv_file.name)

            # 組合新檔案名稱
            filename = f"{branch_id}_{user_id}_{date_time}{file_extension}"
            fs = FileSystemStorage(location=os.path.join(settings.CSV_ROOT, 'restock'))
            filename = fs.save(filename, csv_file)
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
    list_display = ['id', 'Product', 'Restock', 'ExpiryDate', 'Number', 'Remain', 'Branch','Import_price']

@admin.register(RestockDetail_relation)
class RestockDetailRelationAdmin(admin.ModelAdmin):
    list_display = ['id', 'InID', 'OutID', 'Number']

@admin.register(Transpose)
class TransposeAdmin(admin.ModelAdmin):
    list_display = ['id', 'User','BranchsSend','BranchsReceipt','Restock','Time']
    search_fields = ['id', 'User','BranchsSend','BranchsReceipt','Restock','Time']
    list_filter = ['id', 'User','BranchsSend','BranchsReceipt','Restock','Time']
    ordering = ['BranchsSend']
    # inlines = [RestockDetailInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super(TransposeAdmin, self).get_form(request, obj, **kwargs)
        if 'User' in form.base_fields:
            form.base_fields['User'].initial = request.user
            form.base_fields['User'].disabled = True
        return form