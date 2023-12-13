from django.contrib import admin
from .models import ShoppingCart,ShoppingCartDetails,Orders,OrderDetails,OrderLog
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
    list_display = ['id', 'Product', 'Number', 'Time', 'Price', 'Total']
    search_fields = ['id', 'Product', 'Number', 'Time', 'Price', 'Total']
    list_filter = ['id', 'Product', 'Number', 'Time', 'Price', 'Total']
    ordering = ['Time']

# ['Product','Number','Time','Price','Total']
@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display =  ['id', 'User', 'Time', 'Delivery_method', 'Delivery_state', 'Payment_method', 'Payment_time', 'Address', 'Total']
    search_fields = ['User','Time','Delivery_method','Delivery_state','Payment_method','Payment_time','Total']
    list_filter = ['User','Time','Delivery_method','Delivery_state','Payment_method','Payment_time','Total']
    ordering = ['Time']
# ['User','Time','Delivery_method','Delivery_state','Payment_method','Payment_time','Total']

@admin.register(OrderDetails)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'Product', 'Number', 'Price', 'Total']
    search_fields = ['Product','Number','Price','Total']
    list_filter = ['Product','Number','Price','Total']
    ordering = ['Product']

# ['Product','Number','Price','Total']
@admin.register(OrderLog)
class OrderLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'Order', 'User', 'Time', 'Delivery_state']

