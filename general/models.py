import secrets
import string
from datetime import date, timedelta, time, datetime
from django.contrib.auth.models import User
from django.db import models

alphabet = string.digits

def calculate_tracking_number():
    digits = ''.join(secrets.choice(alphabet) for i in range(12))
    # s = "".join(self.vehicle.courier_company.company_name.split())
    tracking_number = digits
    return tracking_number


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
    company_logo = models.ImageField(upload_to='logos', verbose_name='Upload Company logo.', null=True, blank=True)
    company_phone_number = models.CharField(max_length=50)
    company_email = models.EmailField(max_length=64)
    address = models.CharField(max_length=100)
    all1zed_commission = models.FloatField(default=5.0, help_text='Commission charged per Package Sent (In Zambian '
                                                                  'Kwacha)')
    number_of_packages = models.IntegerField(default=0, help_text='Initial number of packages.')

    class Meta:
        verbose_name_plural = 'Courier Companies'

    def __str__(self):
        return self.company_name


class Vehicle(models.Model):
    """
    The actual bus that will be delivering packages.
    """
    courier_company = models.ForeignKey(CourierCompany, on_delete=models.CASCADE)
    vehicle_full_name = models.CharField(max_length=255)
    departure_time = models.TimeField()
    transit_time = models.IntegerField(help_text='Number of hours it takes for vehicle to reach the destination.')

    def __str__(self):
        return self.vehicle_full_name

    class Meta:
        verbose_name_plural = 'Vehicles'


class Package(models.Model):
    """Package to be tracked"""
    tracking_number = models.CharField(max_length=255, editable=False)
    package_value = models.IntegerField(default=0.0, null=True, blank=True)
    processed_by = models.CharField(max_length=255, default='Not Applicable for this package')
    receiver_name = models.CharField(max_length=255)
    receiver_phone_number = models.CharField(max_length=255)
    sender_phone_number = models.CharField(max_length=255)
    delivery_town = models.CharField(max_length=255)
    starting_town = models.CharField(max_length=255, default='Lusaka')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    number_of_packages = models.IntegerField(default=1)
    price = models.FloatField(default=0.0)
    departure_date = models.DateField(blank=True, null=True)
    departure_time = models.TimeField()
    processed_date_time = models.DateTimeField(auto_now_add=True) # Time package was processed.
    transit_date_time = models.DateTimeField(blank=True, null=True) # Time vehicle started moving.
    ready_for_collection_date_time = models.DateTimeField(blank=True, null=True) # Time package becomes ready for collection.
    collected_date_time = models.DateTimeField(blank=True, null=True) # Time package was collected.
    processed_status = models.BooleanField(default=True, blank=True, null=True)
    transit_status = models.BooleanField(default=False, blank=True, null=True)
    transit_message = models.CharField(max_length=255, default='In transit.')
    ready_for_collection_status = models.BooleanField(default=False, blank=True, null=True)
    collected_status = models.BooleanField(default=False, blank=True, null=True)
    current_coordinates = models.CharField(max_length=255, default="0.0, 0.0")
    previous_town = models.CharField(max_length=255, default='...')

    def __str__(self):
        return f"{self.tracking_number} ---> {self.starting_town} - {self.delivery_town}"

    def save(self, *args, **kwargs):
        alphabet = string.ascii_uppercase + string.digits
        self.tracking_number = ''.join(secrets.choice(alphabet) for i in range(10))
        super(Package, self).save(*args, **kwargs)