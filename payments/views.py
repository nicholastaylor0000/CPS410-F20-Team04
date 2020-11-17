from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from scheduler.models import ScheduleEvent

def process_payment(request):
    
    #start = request.session.get('start')
    #event = get_object_or_404(ScheduleEvent, id=start)
    host = request.get_host()

    paypal_dict ={
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': 20.00,
        'item_name': 'Paragalactic Session',#.format(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment_cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'process_payment.html', {'form': form})

@csrf_exempt
def payment_done(request):
    return render(request, 'payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment_cancelled.html')
