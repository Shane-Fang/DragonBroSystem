from django.contrib.auth.views import LoginView
from django.urls import path
# from .views import CustomLoginView
from . import views

urlpatterns = [

    path('register/', views.register, name='register'),
    path('memberprofile/', views.memberprofile, name='memberprofile'),
    path('login/', views.memberlogin,name='login'),
    path('logout/', views.user_logout, name='logout'),
    # path('cgmember/<str:type>/<str:username>/', views.cgmember,name='cgmember'),
    # path('cgmember/<str:type>/', views.cgmember),
]