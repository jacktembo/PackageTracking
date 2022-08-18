from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from .models import Package
from .serializers import PackageSerializer
from django.shortcuts import get_object_or_404, get_list_or_404


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