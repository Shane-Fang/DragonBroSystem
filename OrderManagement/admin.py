from django.contrib import admin
from .models import ShoppingCart,ShoppingCartDetails,Orders,OrderDetails

# Register your models here.
@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['User','Total']
    search_fields = ['User','Total']
    list_filter = ['User','Total']
    # ordering = ['id']

# ['User','Total']
@admin.register(ShoppingCartDetails)
class ShoppingCartDetailsAdmin(admin.ModelAdmin):
    list_display = ['Product','Number','Time','Price','Total']
    search_fields = ['Product','Number','Time','Price','Total']
    list_filter = ['Product','Number','Time','Price','Total']
    ordering = ['Time']

# ['Product','Number','Time','Price','Total']
@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['User','Time','Delivery_method','Delivery_state','Payment_method','Payment_time','Total']
    search_fields = ['User','Time','Delivery_method','Delivery_state','Payment_method','Payment_time','Total']
    list_filter = ['User','Time','Delivery_method','Delivery_state','Payment_method','Payment_time','Total']
    ordering = ['Time']
# ['User','Time','Delivery_method','Delivery_state','Payment_method','Payment_time','Total']

@admin.register(OrderDetails)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ['Product','Number','Price','Total']
    search_fields = ['Product','Number','Price','Total']
    list_filter = ['Product','Number','Price','Total']
    ordering = ['Product']

# ['Product','Number','Price','Total']