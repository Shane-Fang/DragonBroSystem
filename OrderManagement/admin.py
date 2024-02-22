from django.contrib import admin
from .models import ShoppingCart,ShoppingCartDetails,Orders,OrderDetails,OrderLog,OrderDetailsLog
from Product.models import Products,RestockDetail,Restock,RestockDetail_relation
from django.utils.html import format_html,format_html_join
from django.utils.safestring import mark_safe
from import_export.admin import ExportMixin
from import_export import resources, fields
import tablib
from django.http import HttpResponse
import datetime
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.db.models import Prefetch
from django.utils import timezone
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

class TodayFilter(admin.SimpleListFilter):
    title = _('Today')  # 顯示的標題
    parameter_name = 'today'  # URL 參數名稱

    def lookups(self, request, model_admin):
        return (
            ('today', _('Today')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'today':
            today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today_start + datetime.timedelta(days=1)
            return queryset.filter(Time__range=(today_start, today_end))
def calculate_profit(restocks, detail):
    total_profit = 0
    for restock in restocks:
        restock_details = RestockDetail.objects.filter(Restock=restock, Product=detail.Products)
        for restock_detail in restock_details:
            restockDetail_relations = RestockDetail_relation.objects.filter(OutID=restock_detail.pk)
            for restockDetail_relation in restockDetail_relations:
                restock_detail_restocks = RestockDetail.objects.filter(InID=restockDetail_relation.pk)
                for restock_detail_restock in restock_detail_restocks:
                    if restock_detail_restock.Import_price is not None:
                        total_profit += restock_detail_restock.Import_price * restockDetail_relation.Number
    return total_profit
def prepare_row_data(order, detail, total_profit, is_superuser):
    time_no_tz = order.Time.replace(tzinfo=None) if order.Time else order.Time
    profit = (detail.Price - total_profit) * detail.Number
    row = [
        order.id, order.User, time_no_tz, order.get_Delivery_method_display(),
        order.get_Payment_method_display(), order.get_Delivery_state_display(),
        detail.Products, detail.Price, detail.Number, detail.Total, total_profit,
        order.branch
    ]
    if is_superuser:
        row.append(profit)
    return row, detail.Total, profit if is_superuser else 0
def export_to_excel(modeladmin, request, queryset):
    dataset = tablib.Dataset()
    total_price = 0
    super_total_profit = 0
    orders_content_type = ContentType.objects.get_for_model(Orders)

    for order in queryset:
        restocks = Restock.objects.filter(content_type=orders_content_type, object_id=order.id)
        print(OrderDetails.objects.filter(Order=order,Delivery_state=4))
        for detail in OrderDetails.objects.filter(Order=order,Delivery_state=4):
            total_profit = calculate_profit(restocks, detail)
            row, price, profit = prepare_row_data(order, detail, total_profit, request.user.is_superuser)
            dataset.append(row)
            total_price += price
            super_total_profit += profit

    headers = ['訂單編號', '客戶', '下單時間', '運送方式', '付款方式', '訂單狀態', '商品名稱', '商品價格', '訂單數量', '總價', '成本價', '店名']
    if request.user.is_superuser:
        headers.append('利潤')
        dataset.append(['', '', '', '', '', '', '', '', '總價：', total_price, '', '利潤：', super_total_profit])
    else:
        dataset.append(['', '', '', '', '', '', '', '', '總價：', total_price, '', ''])
    dataset.headers = headers

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
    extra = 0
    # max_num = 0
    def get_fields(self, request, obj=None):
        return ['Products', 'Delivery_method', 'Delivery_state', 'Payment_method', 'Payment_time', 'Price','Number', 'Total']
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
        return ['Products', 'Price','Number', 'Total']

# ['Product','Number','Time','Price','Total']
@admin.register(Orders)
class OrdersAdmin(ExportMixin, admin.ModelAdmin):
    list_display =  ['id', 'User', 'Time', 'Delivery_method', 'Delivery_state', 'Payment_method', 'Payment_time', 'Address', 'Total','detail_info']
    search_fields = ['User','Time','Delivery_method','Delivery_state','Payment_method','Payment_time','Total']
    # list_filter = ['User','Time','Delivery_method','Delivery_state','Payment_method','Payment_time','Total']
    list_filter = (MonthFilter,TodayFilter) 
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
    list_display = ['id','get_user', 'Products', 'Number', 'Price', 'Total']
    search_fields = ['Order__User__phone_number']
    list_filter = ['Order__User__phone_number']
    readonly_fields = ('Order','Products', 'Number', 'Price','Total')  
    ordering = ['Products']
    def get_user(self, obj):
        return obj.Order.User
    get_user.short_description = "使用者"

# ['Product','Number','Price','Total']
@admin.register(OrderLog)
class OrderLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'Order', 'User', 'Time', 'Delivery_state']
    readonly_fields = ('Order', 'User', 'Time','Delivery_state')  
@admin.register(OrderDetailsLog)
class OrderDetailsLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'OrderDetails', 'User', 'Time', 'Delivery_state']
    readonly_fields = ('OrderDetails', 'User', 'Time','Delivery_state')  

