"""myfashion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import blog.views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/',include('blog.urls')),
    path('', blog.views.index, name='index'),
    #path('upload/',blog.views.upload,name='upload'),
    path('clothes/',blog.views.cloth_list,name='cloth_list'),
    path('upload/',blog.views.upload_cloth,name='upload_cloth'),
    path('clothes/save/',blog.views.save_cloth,name='save_cloth'),
    path('clothes/result/<int:cloth_id>/',blog.views.result,name='result'),
    path('test/', blog.views.Rec, name='test'),
    path('clothes/Top/',blog.views.cloth_list1,name='cloth_list1'),
    path('clothes/Bottom/',blog.views.cloth_list2,name='cloth_list2'),
    path('clothes/Dress',blog.views.cloth_list3,name='cloth_list3'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
