from django.contrib import admin
from .models import ShoppingCart,ShoppingCartDetails,Orders,OrderDetails,OrderLog
from django.utils.html import format_html,format_html_join
from django.utils.safestring import mark_safe
# Register your models here.
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

# ['Product','Number','Time','Price','Total']
@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display =  ['id', 'User', 'Time', 'Delivery_method', 'Delivery_state', 'Payment_method', 'Payment_time', 'Address', 'Total','detail_info']
    search_fields = ['User','Time','Delivery_method','Delivery_state','Payment_method','Payment_time','Total']
    list_filter = ['User','Time','Delivery_method','Delivery_state','Payment_method','Payment_time','Total']
    readonly_fields = ('User', 'Time', 'Delivery_method','Payment_method','Total')  
    ordering = ['Time']
    def detail_info(self, obj):
        details = OrderDetails.objects.filter(Order=obj)
        # 格式化顯示資料
        return format_html_join(
            mark_safe('<br>'),
            "商品名稱：{} - 價格：{} - 數量：{} - 總價：{}",
            ((detail.Products, detail.Price, detail.Number, detail.Total) for detail in details)
        ) if details else 'No details'
    detail_info.short_description = '訂單明細'
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

