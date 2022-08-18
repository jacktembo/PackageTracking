"""PackageTracking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from datetime import datetime

from django.contrib import admin
from django.urls import path, include

right_now = datetime.now()


# 00:00 - 11:00 - Morning
# 12:00 - 17:00 - Afternoon
#  18:00 - 23:00 - Evening
def message():
    if 0 <= right_now.hour <= 11:
        return 'Good Morning'
    elif 12 <= right_now.hour <= 17:
        return 'Good Afternoon'
    elif 18 <= right_now.hour <= 23:
        return 'Good Evening'


admin.AdminSite.site_header = 'All1Zed Package Tracking'
admin.AdminSite.index_title = f'{message()}. Welcome To All1Zed Package Tracking System.'

urlpatterns = [
    path('', include('users.urls')),
    path('', include('global.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('global/', include('global.urls')),
    path('api/', include('global.urls')),
    path('api/', include('users.urls')),
]
