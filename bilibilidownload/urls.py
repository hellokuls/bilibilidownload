"""bilibilidownload URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
# 公众号：Python进击者
from django.contrib import admin
from django.urls import path,include
from Download import views
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index),
    path('getVideoList/', views.getVideoList),
    path('down_video/', views.down_video),
    path('index2/', views.index2)
]
