from django.contrib import admin
from .models import PendingPaymentApproval

@admin.register(PendingPaymentApproval)
class PendingPaymentApprovalAdmin(admin.ModelAdmin):
    list_display = [
        'courier_company', 'amount', 'reference_number', 'date_time_created', 'phone_number', 'session_uuid'
    ]
    list_filter = [
        'courier_company', 'date_time_created', 'session_uuid'
    ]