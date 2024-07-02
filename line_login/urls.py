from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('login', views.log_in, name='log-in'),
    path('logout', views.log_out, name='log-out'),
    path('enter_phone_number', views.enter_phone_number, name='enter_phone_number'),
]