from django.urls import path
from . import views
# OrderManagement
urlpatterns = [
    # 其他 URL 配置...
    path('cart/', views.cart, name='cart'),
    path('delete_from_cart/', views.delete_from_cart, name='delete_from_cart'),
    path('update_cart_item/', views.update_cart_item, name='update_cart_item'),
    path('cartorder/',views.cartorder,name='cartorder'),
    path('cartok/',views.cartok,name='cartok'),
    path('submit_order/',views.submit_order,name='submit_order'),
    path('past_orders/', views.past_orders, name='past_orders'),
    path('past_orders/<int:stateId>', views.past_orders, name='past_orders'),
    # path('past_order_details/<int:order_id>/', views.past_order_details, name='past_order_details'),
    # path('ajax/order_status/<int:stateId>/', views.order_status, name='order_status'),

]