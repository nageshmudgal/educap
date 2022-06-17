from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     path("login",views.login,name='login'),
     path('logout',views.logout,name='logout'),
     path('signup/',views.signup,name='signup'),
     path('', views.homes ,name='homes'),
     path('profileupdate',views.profileupdate,name='profileupdate'),
     path('changepass',views.changepass,name='changepass'),
]