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
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

admin.AdminSite.site_header = 'Package Tracking'
admin.AdminSite.index_title = 'Welcome To All1Zed Package Tracking System'

urlpatterns = [
    path('', views.index, name='index'),
    path('packages', views.PackageList.as_view()),
    path('packages/<tracking_number>', views.PackageDetail.as_view()),
    path('packages/location/update', views.PackagesUpdateLocation.as_view()),
    path('courier-companies', views.CourierCompanyList.as_view()),
    path('courier-companies/<int:id>', views.CourierCompanyDetail.as_view()),
    path('vehicles', views.VehicleList.as_view()),
    path('total-sales', views.TotalSales.as_view()),
    path('total-sales/<int:vehicle_id>', views.TotalSales.as_view()),
    path('total-sales-count', views.TotalSalesCount.as_view()),
    path('total-sales-count/<int:vehicle_id>', views.TotalSalesCount.as_view()),
    path('sort', views.Sorting.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
