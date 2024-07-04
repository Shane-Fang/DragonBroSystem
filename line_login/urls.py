from django.urls import path
from . import views

urlpatterns = [
    path('enter_phone_number', views.enter_phone_number, name='enter_phone_number'),
]