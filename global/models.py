import secrets
import string
from datetime import date, timedelta, time, datetime
from django.contrib.auth.models import User
from django.db import models


class CourierCompany(models.Model):
    """A company that owns vehicle(s)

    Args:
        models ([type]): [description]

    Returns:
        [type]: [description]
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Login Username')  # Admin user account for the Bus Company.
    company_name = models.CharField(max_length=50)
    company_phone_number = models.CharField(max_length=50)
    company_email = models.EmailField(max_length=64)
    address = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Courier Companies'

    def __str__(self):
        return self.company_name


class Vehicle(models.Model):
    """
    The actual bus that will be delivering packages.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courier_company = models.ForeignKey(CourierCompany, on_delete=models.CASCADE)
    vehicle_full_name = models.CharField(max_length=255)
    departure_time = models.TimeField(default=datetime.now().time())
    transit_time = models.TimeField(default=datetime.now().time())

    def __str__(self):
        return self.vehicle_full_name

    class Meta:
        verbose_name_plural = 'Vehicles'


class Package(models.Model):
    """Package to be tracked"""
    tracking_number = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    receiver_name = models.CharField(max_length=255)
    receiver_phone_number = models.CharField(max_length=255)
    sender_phone_number = models.CharField(max_length=255)
    delivery_destination = models.CharField(max_length=255)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    number_of_packages = models.IntegerField(default=1)
    price = models.FloatField(default=0.0)
    departure_date = models.DateField()
    departure_time = models.DateField()
    date_time_received = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255, default="0.0, 0.0")

    def save(self, *args, **kwargs):
        alphabet = string.digits
        digits = ''.join(secrets.choice(alphabet) for i in range(8))
        s = "".join(self.vehicle.courier_company.company_name.split())
        self.tracking_number = f'{s[:2]}' + digits
        super(Package, self).save(*args, **kwargs)
