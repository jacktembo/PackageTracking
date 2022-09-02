import datetime

from django.db.models import Sum
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Package, Vehicle, CourierCompany
from .serializers import PackageSerializer, VehicleSerializer, CourierCompanySerializer
from utils import sms, phone_numbers


today = datetime.datetime.today()


class PackageList(ListCreateAPIView):
    def get_queryset(self):
        return Package.objects.filter(vehicle__courier_company__user=self.request.user)

    def get_serializer_class(self):
        return PackageSerializer

    def create(self, request, *args, **kwargs):
        sender_phone_number = self.request.data['sender_phone_number']
        receiver_phone_number = self.request.data['receiver_phone_number']
        price = self.request.data['price']
        receiver_name = self.request.data['receiver_name']
        starting_town = self.request.data['starting_town']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        tracking_number = serializer.data[next(iter(serializer.data))]
        receiver_message = f"Dear {receiver_name}, your package has been received at {starting_town} station and processed " \
                           f"for dispatch. Tracking No. FM{tracking_number} Courier charge K{price}. Check your package status at https://packages.all1zed.com. "
        sender_message = f"Dear Customer, the package you are sending has been processed " \
                           f"for dispatch. Tracking No. FM{tracking_number} Courier charge K{price}. Check your package status at https://packages.all1zed.com. "
        sms.send_sms(receiver_phone_number, receiver_message)
        sms.send_sms(sender_phone_number, sender_message)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PackageDetail(RetrieveUpdateDestroyAPIView):
    lookup_field = 'tracking_number'

    def get_serializer_class(self):
        return PackageSerializer

    def get_queryset(self):
        return Package.objects.filter(vehicle__courier_company__user=self.request.user)


class VehicleList(ListCreateAPIView):
    def get_queryset(self):
        return Vehicle.objects.filter(courier_company__user=self.request.user)

    def get_serializer_class(self):
        return VehicleSerializer


class CourierCompanyList(ListCreateAPIView):
    def get_queryset(self):
        return CourierCompany.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        return CourierCompanySerializer


class TotalSales(APIView):
    """
    Get total sales for whole company or specified bus.
    """

    def get(self, request):
        vehicle_id = self.request.query_params.get('vehicle_id', None)
        if vehicle_id == None:
            result = Package.objects.filter(departure_date=today,
                                          vehicle__courier_company__user=self.request.user).aggregate(Sum('price')).get('price__sum')
            return Response(result)
        else:
            result = Package.objects.filter(departure_date=today, vehicle__courier_company__user=self.request.user,
                                          vehicle__id=int(vehicle_id)).aggregate(Sum('price')).get('price__sum')
            return Response(result)


class TotalSalesCount(APIView):
    def get(self, request):
        vehicle_id = self.request.query_params.get('vehicle_id', None)
        if vehicle_id == None:
            result = Package.objects.filter(departure_date=today,
                                          vehicle__courier_company__user=self.request.user).count()
            return Response(result)

        else:
            result = Package.objects.filter(departure_date=today, vehicle__courier_company__user=self.request.user,
                                          vehicle__id=int(vehicle_id)).count()
            return Response(result)
