import datetime

from django.db.models import Sum
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Package, Vehicle, CourierCompany
from .serializers import PackageSerializer, VehicleSerializer, CourierCompanySerializer

today = datetime.datetime.today()


class PackageList(ListCreateAPIView):
    def get_queryset(self):
        return Package.objects.all()

    def get_serializer_class(self):
        return PackageSerializer


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
