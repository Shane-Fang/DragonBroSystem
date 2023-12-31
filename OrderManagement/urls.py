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
]