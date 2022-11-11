from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import APIView, api_view
from django.contrib.auth import authenticate
from PackageTracking.models import PricingPlan
from utils import phone_numbers, kazang, sms
from general.models import *
from utils.models import PendingPaymentApproval
import pytz

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
        cost = float(cost) + (0.02 * float(cost))
        if phone_numbers.get_network(phone_number).lower() == 'airtel':
            r = kazang.airtel_pay_payment(phone_number, cost * 100)
            if r.get('response_code', None) == '0':
                del r['balance']
                r['message'] = 'Please approve the transaction on your phone.'
                r['status'] = 'successful'
                r['reference_number'] = r['airtel_reference']
                PendingPaymentApproval.objects.create(
                    session_uuid=kazang.session_uuid, product_id='5392',
                    date_time_created=datetime.now(), phone_number=phone_number,
                    reference_number=r['airtel_reference'], amount=cost,
                    plan_id=plan_id, courier_company=courier_company
                )

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
                PendingPaymentApproval.objects.create(
                    session_uuid=kazang.session_uuid, product_id='5392',
                    date_time_created=datetime.now(), phone_number=phone_number,
                    reference_number=r['airtel_reference'], amount=cost,
                    plan_id=plan_id, courier_company=courier_company
                )
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
                PendingPaymentApproval.objects.create(
                    session_uuid=kazang.session_uuid, product_id='5392',
                    date_time_created=datetime.now(), phone_number=phone_number,
                    reference_number=r['airtel_reference'], amount=cost,
                    plan_id=plan_id, courier_company=courier_company
                )
                return Response({'status': 'successful', 'message': 'zamtel payment was successful'})
            else:
                return Response({'status': 'failed', 'message': 'zamtel payment failed.'})



class TopUpQuery(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number', None)
        amount = (float(request.data.get('amount', None)) * 100) + (0.02 * (float(request.data.get('amount', None)) * 100))
        reference_number = request.data.get('reference_number', None)
        if phone_numbers.get_network(phone_number).lower() == 'airtel':
            r = kazang.airtel_pay_query(phone_number, amount, reference_number)
            # del r['balance']
            if r.get('response_code', '1') == '0':
                plan_id = request.data.get('plan_id', None)
                plan = PricingPlan.objects.get(id=int(plan_id))
                courier_company = CourierCompany.objects.filter(user=request.user).first()
                remaining_packages = courier_company.number_of_packages
                c = CourierCompany.objects.filter(user=request.user).first()
                c.number_of_packages = remaining_packages + plan.number_of_packages
                c.save()
                return Response({'status': 'successful', 'message': 'airtel payment was successful.'})
            else:
                return Response({'status': 'failed', 'message': 'airtel payment failed.'})

        elif phone_numbers.get_network(phone_number).lower() == 'mtn':
            r = kazang.mtn_debit_approval(phone_number, amount, reference_number)
            if r.get('response_code', '1') == '0':
                confirmation_number = r['confirmation_number']
                approval_confirm = kazang.mtn_debit_approval_confirm(phone_number, amount, confirmation_number)
                if approval_confirm.get('response_code', '1') == '0':
                    plan_id = request.data.get('plan_id', None)
                    plan = PricingPlan.objects.get(id=int(plan_id))
                    courier_company = CourierCompany.objects.filter(user=request.user).first()
                    remaining_packages = courier_company.number_of_packages
                    c = CourierCompany.objects.filter(user=request.user).first()
                    c.number_of_packages = remaining_packages + plan.number_of_packages
                    c.save()
                    return Response({'status': 'successful', 'message': 'MTN payment was successful.'})

                else:
                    return Response({'status': 'failed', 'message': 'MTN payment failed.'})

            return Response({'status': 'failed', 'message': 'Please approve the transaction on your mobile device.'})



@api_view()
def topup_query_api(request, pending_approval_id):
    pending = PendingPaymentApproval.objects.get(id=int(pending_approval_id))
    phone_number = pending.phone_number
    amount = (float(pending.amount) * 100) + (0.02 * (float(pending.amount) * 100))
    reference_number = pending.reference_number
    if phone_numbers.get_network(phone_number).lower() == 'airtel':
        r = kazang.airtel_pay_query(phone_number, amount, reference_number)
        # del r['balance']
        if r.get('response_code', '1') == '0':
            plan_id = pending.plan_id
            plan = PricingPlan.objects.get(id=int(plan_id))
            courier_company = CourierCompany.objects.filter(user=request.user).first()
            remaining_packages = courier_company.number_of_packages
            c = CourierCompany.objects.filter(user=request.user).first()
            c.number_of_packages = remaining_packages + plan.number_of_packages
            c.save()
            # return Response({'status': 'successful', 'message': 'airtel payment was successful.'})
        else:
            pass
            # return Response({'status': 'failed', 'message': 'airtel payment failed.'})

    elif phone_numbers.get_network(phone_number).lower() == 'mtn':
        r = kazang.mtn_debit_approval(phone_number, amount, reference_number)
        if r.get('response_code', '1') == '0':
            confirmation_number = r['confirmation_number']
            approval_confirm = kazang.mtn_debit_approval_confirm(phone_number, amount, confirmation_number)
            if approval_confirm.get('response_code', '1') == '0':
                plan_id = pending.plan_id
                plan = PricingPlan.objects.get(id=int(plan_id))
                courier_company = CourierCompany.objects.filter(user=request.user).first()
                remaining_packages = courier_company.number_of_packages
                c = CourierCompany.objects.filter(user=request.user).first()
                c.number_of_packages = remaining_packages + plan.number_of_packages
                c.save()
                # return Response({'status': 'successful', 'message': 'MTN payment was successful.'})

            else:
                pass
                # return Response({'status': 'failed', 'message': 'MTN payment failed.'})

        # return Response({'status': 'failed', 'message': 'Please approve the transaction on your mobile device.'})
    utc = pytz.UTC
    pending_transaction_age = datetime.now().replace(tzinfo=utc) - pending.date_time_created.replace(tzinfo=utc)
    if pending_transaction_age > timedelta(seconds=20):
        pending.delete()


def process_pending(request):
    pendings = PendingPaymentApproval.objects.all()
    for pending in pendings:
        topup_query_api(request, pending.id)
    return HttpResponse('Done')
