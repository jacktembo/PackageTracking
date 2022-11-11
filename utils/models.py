from django.db import models

from general.models import CourierCompany


class PendingPaymentApproval(models.Model):
    session_uuid = models.CharField(max_length=255)
    product_id = models.CharField(max_length=255)
    date_time_created = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=255)
    reference_number = models.CharField(max_length=255)
    amount = models.FloatField()
    plan_id = models.IntegerField()
    courier_company = models.ForeignKey(CourierCompany, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.phone_number} - {self.amount}"