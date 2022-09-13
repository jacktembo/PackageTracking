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

    def from_town(self, package: Package):
        return package.starting_town

    def status(self, package: Package):
        return "Collected" if package.collected_status else "Not Collected"

    list_display = [
        'tracking_number',  'receiver_name', 'receiver_phone_number',
        'vehicle', 'from_town', 'delivery_town', 'departure_date', 'departure_time',
        'price', 'status',

    ]
