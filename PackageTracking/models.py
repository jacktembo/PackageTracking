from django.db import models


class KazangSession(models.Model):
    """
    Kazang (Content Ready Session).
    """
    session_uuid = models.CharField(max_length=255, editable=False)
    date_time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.session_uuid


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('cash_in', 'cash_in'), ('payment', 'payment'),
    ]
    TRANSACTION_STATUS = [
        ('successful', 'successful'), ('failed', 'failed'),
    ]
    """
    A Transaction that happens on the system.
    """
    name = models.CharField(max_length=100, blank=True, null=True, default='..')
    session_uuid = models.CharField(max_length=255)
    date_time_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=TRANSACTION_STATUS)
    product_id = models.IntegerField()
    amount = models.FloatField()
    phone_number = models.CharField(max_length=15)
    type = models.CharField(choices=TRANSACTION_TYPES, max_length=255)
    request_reference = models.CharField(max_length=255, null=True, blank=True)
    provider_reference = models.CharField(max_length=255)

    def __str__(self):
        return f"Product ID {self.product_id} - {self.status}"


class PricingPlan(models.Model):
    tier_name = models.CharField(max_length=255, help_text='Pricing Plan Tier Name e.g Gold Standard Plan.')
    number_of_packages = models.IntegerField()

    def __str__(self):
        return self.tier_name
