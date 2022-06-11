from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     path('', views.home ,name='home'),
     path("login",views.login,name='login'),
     path('logout',views.logout,name='logout'),
     path("deleteinstance",views.deleteinstance,name='deleteinstance'),
     path("course",views.course,name='course'),
     path("viewcourse",views.viewcourse,name='viewcourse'),
]