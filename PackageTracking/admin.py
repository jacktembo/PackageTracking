# from django.contrib import admin
# from .models import KazangSession, Transaction, PricingPlan
#
# @admin.register(KazangSession)
# class KazangSesionAdmin(admin.ModelAdmin):
#     list_display = [
#         'date_time_created', 'session_uuid'
#     ]
#     list_filter = ['date_time_created']
#
#
# @admin.register(Transaction)
# class TransactionAdmin(admin.ModelAdmin):
#     list_display = [
#         'phone_number', 'amount', 'status', 'session_uuid', 'request_reference',
#         'product_id', 'date_time_created'
#     ]
#
#     list_filter = ['status', 'date_time_created']
#
#
# @admin.register(PricingPlan)
# class PricingPlanAdmin(admin.ModelAdmin):
#     list_display = ['tier_name', 'number_of_packages']
