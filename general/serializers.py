from django.contrib.auth.models import User
from rest_framework import serializers
import pytz
from .models import Package, Vehicle, CourierCompany

utc = pytz.UTC
from datetime import datetime, timedelta


class PackageSerializer(serializers.ModelSerializer):
    package_tracking_number = serializers.SerializerMethodField(method_name='the_tracking_number')
    # current_coordinates = serializers.SerializerMethodField(method_name='the_converted_coordinates')
    balance = serializers.SerializerMethodField(method_name='the_balance')
    vehicle_id = serializers.SerializerMethodField(method_name='the_vehicle_id')
    vehicle_name = serializers.SerializerMethodField(method_name='the_vehicle_name')
    company_name = serializers.SerializerMethodField(method_name='the_company_name')
    in_transit_message = serializers.SerializerMethodField(method_name='the_transit_message')


    def the_tracking_number(self, package: Package):
        return package.tracking_number

    def the_converted_coordinates(self, package: Package):
        return [float(i) for i in package.current_coordinates.split(', ')]

    def the_balance(self, package: Package):
        return package.vehicle.courier_company.number_of_packages

    def the_vehicle_id(self, package: Package):
        return package.vehicle.id

    def the_vehicle_name(self, package: Package):
        return package.vehicle.vehicle_full_name

    def the_company_name(self, package: Package):
        return package.vehicle.courier_company.company_name

    def the_transit_message(self, package: Package):
        return 'In Transit' if datetime.now().replace(tzinfo=utc) > (datetime(package.departure_date.year, package.departure_date.month, package.departure_date.day) + timedelta(hours=package.departure_time.hour)).replace(tzinfo=utc) else '...'

    class Meta:
        model = Package
        fields = [
            'package_tracking_number',
            'processed_by', 'package_value',
            'vehicle_id', 'vehicle_name', 'company_name',
            'balance', 'receiver_name', 'receiver_phone_number', 'sender_phone_number',
            'delivery_town', 'starting_town', 'vehicle', 'number_of_packages',
            'price', 'departure_date', 'departure_time', 'processed_date_time',
            'transit_date_time', 'ready_for_collection_date_time', 'collected_date_time',
            'processed_status', 'transit_status', 'ready_for_collection_status',
            'collected_status', 'current_coordinates', 'in_transit_message',
            'starting_town_coordinates', 'destination_town_coordinates',
        ]


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            'id', 'courier_company', 'vehicle_full_name', 'departure_time',
            'transit_time',
        ]


class CourierCompanySerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField(method_name='company_image')
    packages_remaining = serializers.SerializerMethodField(method_name='the_packages_remaining')

    def company_image(self, courier_company: CourierCompany):
        return 'https://packages.pridezm.com' + courier_company.company_logo.url if courier_company.company_logo else 'Company did not upload Logo.'

    def the_packages_remaining(self, courier_company: CourierCompany):
        return courier_company.number_of_packages

    class Meta:
        model = CourierCompany
        fields = [
            'packages_remaining',
            'logo', 'company_name', 'company_phone_number', 'company_email',
            'address', 'all1zed_commission'
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email'
        ]
