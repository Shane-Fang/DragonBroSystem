from django.urls import path
from . import views

urlpatterns = [
    # 其他 URL 配置...
    path('<int:branch>', views.products_view, name='products_view'),  
    path('<int:branch>/<int:detail>', views.detail, name='detail'),  
    path('get_branches/', views.get_branches, name='get_branches'),
    path('add_to_cart_view/<int:branch>/<int:product_id>', views.add_to_cart_view, name='add_to_cart_view'),
    path('get-productss/<int:branch_id>/', views.get_products_by_branch, name='get-products-by-branch'),
    # 其他 URL 配置...
]