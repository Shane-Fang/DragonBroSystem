from django.contrib import admin
from .models import ShoppingCart,ShoppingCartDetails,Orders,OrderDetails,OrderLog
from Product.models import Products
from django.utils.html import format_html,format_html_join
from django.utils.safestring import mark_safe
from import_export.admin import ExportMixin
from import_export import resources, fields
import tablib
from django.http import HttpResponse
import datetime
from django.utils.translation import gettext_lazy as _
# Register your models here.
class MonthFilter(admin.SimpleListFilter):
    title = _('month')  # 顯示的標題
    parameter_name = 'month'  # URL 參數名稱
    def lookups(self, request, model_admin):
        return (
            ('1', _('January')),
            ('2', _('February')),
            ('3', _('March')),
            ('4', _('April')),
            ('5', _('May')),
            ('6', _('June')),
            ('7', _('July')),
            ('8', _('August')),
            ('9', _('September')),
            ('10', _('October')),
            ('11', _('November')),
            ('12', _('December')),
        )

    def queryset(self, request, queryset):
        if self.value():
            year = datetime.date.today().year
            return queryset.filter(Time__year=year, Time__month=self.value())
        return queryset
def export_to_excel(modeladmin, request, queryset):
    dataset = tablib.Dataset()
       
    total_price = 0  # 初始化總計變量
    total_profit=0
    for order in queryset:
        # 確保時間沒有時區信息
        time_no_tz = order.Time.replace(tzinfo=None) if order.Time else order.Time
        details = OrderDetails.objects.filter(Order=order)
        if details:
            for detail in details:
                # product = Products.objects.filter(Item_name=detail.Products)
                if request.user.is_superuser:
                    profit=(detail.Price-detail.Products.Import_price)*detail.Number
                    dataset.append([order.id,
                                    order.User,
                                    time_no_tz,
                                    order.get_Delivery_method_display(),
                                    order.get_Payment_method_display(),
                                    order.get_Delivery_state_display(),
                                    detail.Products,
                                    detail.Price,
                                    detail.Number,
                                    detail.Total,
                                    detail.Products.Import_price,
                                    order.branch,
                                    profit])
                    total_price += detail.Total  # 累加 Price
                    total_profit +=  profit
                else:
                    dataset.append([order.id,
                                    order.User,
                                    time_no_tz,
                                    order.get_Delivery_method_display(),
                                    order.get_Payment_method_display(),
                                    order.get_Delivery_state_display(),
                                    detail.Products,
                                    detail.Price,
                                    detail.Number,
                                    detail.Total,
                                    detail.Products.Import_price,
                                    order.branch
                                    ])
                    total_price += detail.Total  # 累加 Price
    if request.user.is_superuser:
        dataset.headers = ['訂單編號', '客戶', '下單時間', '運送方式','付款方式','訂單狀態', '商品名稱', '商品價格', '訂單數量', '總價','成本價','店名','利潤']
        dataset.append(['', '', '', '', '', '', '', '', '總價：', total_price, '', '利潤：', total_profit])
    else:
        dataset.headers = ['訂單編號', '客戶', '下單時間', '運送方式','付款方式','訂單狀態', '商品名稱', '商品價格', '訂單數量', '總價','成本價','店名']
        dataset.append(['', '', '', '', '', '', '', '', '總價：', total_price, '', ''])
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="orders_with_details.xlsx"'
    return response

export_to_excel.short_description = "報表下載"




@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['id', 'User', 'Total']
    search_fields = ['id', 'User', 'Total']
    list_filter = ['id', 'User', 'Total']
    # ordering = ['id']

# ['User','Total']
@admin.register(ShoppingCartDetails)
class ShoppingCartDetailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'Products', 'Number', 'Time']
    search_fields = ['id', 'Products', 'Number', 'Time']
    list_filter = ['id', 'Products', 'Number', 'Time']
    ordering = ['Time']

class OrderDetailsInline(admin.TabularInline):# 或者使用 admin.StackedInline
    model = OrderDetails
    extra = 1
    # max_num = 0
    def get_fields(self, request, obj=None):
        return ['Products', 'Delivery_method', 'Delivery_state', 'Payment_method', 'Payment_time', 'Price', 'Total']
    def get_formset(self, request, obj=None, **kwargs):
        formset = super(OrderDetailsInline, self).get_formset(request, obj, **kwargs)
        for form in formset.form.base_fields:
            if form == 'Branch':
                formset.form.base_fields[form].disabled = True
                formset.form.base_fields[form].initial = request.user.branch
        return formset

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        return ['Products', 'Price', 'Total']

# ['Product','Number','Time','Price','Total']
@admin.register(Orders)
class OrdersAdmin(ExportMixin, admin.ModelAdmin):
    list_display =  ['id', 'User', 'Time', 'Delivery_method', 'Delivery_state', 'Payment_method', 'Payment_time', 'Address', 'Total','detail_info']
    search_fields = ['User','Time','Delivery_method','Delivery_state','Payment_method','Payment_time','Total']
    # list_filter = ['User','Time','Delivery_method','Delivery_state','Payment_method','Payment_time','Total']
    list_filter = (MonthFilter,) 
    readonly_fields = ('User', 'Time', 'Delivery_method','Payment_method','Total')  
    ordering = ['Time']
    inlines = [OrderDetailsInline]
    actions = [export_to_excel]
    def detail_info(self, obj):
        details = OrderDetails.objects.filter(Order=obj)
        # 格式化顯示資料
        return format_html_join(
            mark_safe('<br>'),
            "商品名稱：{} - 價格：{} - 數量：{} - 總價：{}",
            ((detail.Products, detail.Price, detail.Number, detail.Total) for detail in details)
        ) if details else 'No details'
    detail_info.short_description = '訂單明細'
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # 如果是超级用户，返回所有订单
        return qs.filter(branch=request.user.branch) 
# ['User','Time','Delivery_method','Delivery_state','Payment_method','Payment_time','Total']

@admin.register(OrderDetails)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'Products', 'Number', 'Price', 'Total']
    search_fields = ['Products','Number','Price','Total']
    list_filter = ['Products','Number','Price','Total']
    readonly_fields = ('Order','Products', 'Number', 'Price','Total')  
    ordering = ['Products']

# ['Product','Number','Price','Total']
@admin.register(OrderLog)
class OrderLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'Order', 'User', 'Time', 'Delivery_state']
    readonly_fields = ('Order', 'User', 'Time','Delivery_state')  

