from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('',views.user_login),
    path('register',views.user_register,name='register'),
    path('adminlogin',views.admin_login,name='adminlogin'),
    path('userhome',views.userhome,name='userhome'),
    path('uselogout',views.userlogout,name='userlogout'),
    path('adminlogout',views.adminlogout,name='adminlogout'),
    path('adminhome',views.adminhome,name='adminhome'),
    path('userlist',views.userlist,name='userlist'),
    path('updation',views.updation,name='updation'),
    path('do_udpation',views.do_udpation),
    path('deletion',views.deletion),
    path('searching',views.searching),
    path('adduser',views.adduser)
]