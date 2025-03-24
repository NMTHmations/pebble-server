"""
URL configuration for pebbleLeaderboard project.

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
from django.urls import path
from Leaderboard import views
from . import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name="index"),
    path('data/<slug:slug>',views.data),
    path('api/getlist',views.getList),
    path('api/getdata/<slug:slug>',views.getThrow),
    path('api/setdata/',views.insertThrow,name="setdata"),
    path('api/upload-video/<str:filename>/', views.VideoUpload.as_view(), name="uploadVideo"),
]

if settings.DEBUG:  # Only for development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
