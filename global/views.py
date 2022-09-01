from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Package, Vehicle
from .serializers import PackageSerializer, VehicleSerializer


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
        return Package.objects.all()


class VehicleList(ListCreateAPIView):
    def get_queryset(self):
        return Vehicle.objects.filter(courier_company__user=self.request.user)

    def get_serializer_class(self):
        return VehicleSerializer
