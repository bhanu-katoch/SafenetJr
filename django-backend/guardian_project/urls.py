"""
URL configuration for guardian_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from guardian.views import home,get_child_id
from history.views import upload_history

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",home,name="home"),
    path("api/get-child-id/",get_child_id,name="get-child-id"),
    path('api/upload_history/',upload_history, name='upload_history'),

    path('guardian/', include('guardian.urls')),
    path('history/', include('history.urls')), 
]
