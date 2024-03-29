"""educap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
1. Add an import: from my_app import views
2. Add a URL to urlpatterns: path('', views.home, name='home')
Class-based views
1. Add an import: from other_app.views import Home
2. Add a URL to urlpatterns: path('', Home.as_view(), name='home')
Including another URLconf
1. Import the include() function: from django.urls import include, path
2. Add a URL to urlpatterns: path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='index'),
    path('student/',include('student.urls')),
    path('viewcourse', views.viewcourse,name='viewcourse'),
    path('nsearch', views.nsearch,name='nsearch'),
    path('asearch', views.asearch,name='asearch'),
    path('vsearch', views.vsearch,name='vsearch'),
    path('vlsearch', views.vlsearch,name='vlsearch'),
    path('syllabus',views.syllabus,name='syllabus'),
    path('faculty/', include('faculty.urls')),
    path('adminmodule/', include('adminmodule.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,
document_root=settings.STATIC_ROOT)