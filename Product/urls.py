from django.urls import path
from . import views

urlpatterns = [
    # 其他 URL 配置...
    path('', views.products_view, name='products_view'),  # 与商品浏览视图关联的 URL
    # 其他 URL 配置...
]