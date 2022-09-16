from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import APIView

from PackageTracking.models import PricingPlan
from utils import phone_numbers, kazang, sms
from general.models import *


class PricingPlanView(APIView):
    def get(self, request):
        """
        Pricing plans available for courier companies to top up their balance.
        :param request:
        :return: list of pricing plans
        """
        courier_company = CourierCompany.objects.filter(user=request.user).first()
        price_per_package = courier_company.all1zed_commission
        pricing_plans = PricingPlan.objects.all()
        global data
        data = [{
            'id': plan.pk, 'number_of_packages': plan.number_of_packages,
            'price': price_per_package * plan.number_of_packages
        } for plan in pricing_plans]
        return Response(data)


class AccountTopUp(APIView):
    def post(self, request):
        plan_id = request.data.get('plan_id', None)
        phone_number = request.data.get('phone_number', None)
        plan = PricingPlan.objects.get(id=int(plan_id))
        courier_company = CourierCompany.objects.filter(user=request.user).first()
        price_per_package = courier_company.all1zed_commission
        cost = price_per_package * plan.number_of_packages
        if phone_numbers.get_network(phone_number).lower() == 'airtel':
            r = kazang.airtel_pay_payment(phone_number, cost * 100)
            if r.get('response_code', None) == '0':
                del r['balance']
                r['message'] = 'Please approve the transaction on your phone.'
                r['status'] = 'successful'
                r['reference_number'] = r['airtel_reference']
                return Response(r)
            else:
                return Response({'status': 'failed', 'message': 'payment prompt was not sent to a mobile device. Please try again.'})

        elif phone_numbers.get_network(phone_number).lower() == 'mtn':
            r = kazang.mtn_debit(phone_number, cost * 100)
            if r.get('response_code', None) == '0':
                del r['balance']
                r['message'] = 'Please approve the transaction on your mobile device.'
                r['status'] = 'successful'
                r['reference_number'] = r['supplier_transaction_id']
                return Response(r)

        elif phone_numbers.get_network(phone_number).lower() == 'zamtel':
            r = kazang.zamtel_money_pay(phone_number, cost * 100)
            del r['balance']
            r['message'] = 'Please approve the transaction on your mobile device.'
            plan_id = request.data.get('plan_id', None)
            plan = PricingPlan.objects.get(id=int(plan_id))
            courier_company = CourierCompany.objects.filter(user=request.user).first()
            remaining_packages = courier_company.number_of_packages
            CourierCompany.objects.filter(
                user=request.user).first().number_of_packages = remaining_packages + plan.number_of_packages.save()
            if r.get('response_code', None) == '0':
                return Response({'status': 'successful', 'message': 'zamtel payment was successful'})
            else:
                return Response({'status': 'failed', 'message': 'zamtel payment failed.'})



class TopUpQuery(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number', None)
        amount = int(request.data.get('amount', None)) * 100
        reference_number = request.data.get('reference_number', None)
        if phone_numbers.get_network(phone_number).lower() == 'airtel':
            r = kazang.airtel_pay_query(phone_number, amount, reference_number)
            del r['balance']
            if r.get('response_code', '1') == '0':
                plan_id = request.data.get('plan_id', None)
                plan = PricingPlan.objects.get(id=int(plan_id))
                courier_company = CourierCompany.objects.filter(user=request.user).first()
                remaining_packages = courier_company.number_of_packages
                CourierCompany.objects.filter(user=request.user).first().number_of_packages = remaining_packages + plan.number_of_packages.save()
                return Response({'status': 'successful', 'message': 'airtel payment was successful.'})
            else:
                return Response('Payment was not successful')

