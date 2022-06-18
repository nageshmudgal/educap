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
     path("assignment",views.assignment,name='assignment'),
     path("notes",views.notes,name='notes'),
     path("video",views.video,name='video'),
     path("editCourse",views.editCourse,name='editCourse'),
     path("editassignment",views.editassignment,name='editassignment'),
     path("editNotes",views.editNotes,name='editNotes'),
     path("editvideo",views.editvideo,name='editvideo'),
     path("viewcourse",views.viewcourse,name='viewcourse'),
]