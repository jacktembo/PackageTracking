from rest_framework import serializers

from .models import Package, Vehicle, CourierCompany


class PackageSerializer(serializers.ModelSerializer):
    package_tracking_number = serializers.SerializerMethodField(method_name='the_tracking_number')
    current_coordinates = serializers.SerializerMethodField(method_name='the_converted_coordinates')
    balance = serializers.SerializerMethodField(method_name='the_balance')

    def the_tracking_number(self, package: Package):
        return package.tracking_number

    def the_converted_coordinates(self, package: Package):
        return [float(i) for i in package.current_coordinates.split(', ')]

    def the_balance(self, package: Package):
        return package.vehicle.courier_company.number_of_packages

    class Meta:
        model = Package
        fields = [
            'package_tracking_number', 'balance', 'receiver_name', 'receiver_phone_number', 'sender_phone_number',
            'delivery_town', 'starting_town', 'vehicle', 'number_of_packages',
            'price', 'departure_date', 'departure_time', 'processed_date_time',
            'transit_date_time', 'ready_for_collection_date_time', 'collected_date_time',
            'processed_status', 'transit_status', 'ready_for_collection_status',
            'collected_status', 'current_coordinates', 'transit_message'
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

    def company_image(self, courier_company: CourierCompany):
        return 'https://packages.pridezm.com' + courier_company.company_logo.url if courier_company.company_logo else 'Company did not upload Logo.'

    class Meta:
        model = CourierCompany
        fields = [
            'logo', 'company_name', 'company_phone_number', 'company_email',
            'address', 'all1zed_commission'
        ]
