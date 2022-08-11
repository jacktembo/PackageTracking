from django.contrib import admin
from .models import *


@admin.register(CourierCompany)
class BusCompanyAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'company_phone_number', 'company_email', 'address']


@admin.register(Vehicle)
class BusAdmin(admin.ModelAdmin):
    list_display = ['vehicle_full_name', 'courier_company']


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = [
        'tracking_number', 'status', 'receiver_name', 'receiver_phone_number',
        'vehicle', 'delivery_destination', 'departure_date', 'departure_time'
    ]