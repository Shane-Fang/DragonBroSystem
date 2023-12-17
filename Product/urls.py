from django.urls import path
from . import views

urlpatterns = [
    # 其他 URL 配置...
    path('', views.products_view, name='products_view'),  
    path('get_branches/', views.get_branches, name='get_branches'),
    # 其他 URL 配置...
]