from django.shortcuts import redirect, render
from django.http import HttpResponse
from zeep import Client
from .models import Vocher
from django.utils.crypto import get_random_string

# Create your views here.


MERCHANT = ''
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
amount = 10000  # Toman / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
CallbackURL = 'http://localhost:8000/zarinpal/verify/' # Important: need to edit for realy server.

def send_request(request):
    result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))




def verify(request):
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            unique = get_random_string(length=32)
            f=Vocher(unique_id=unique)
            f.save()
            vochers= Vocher.objects.get(unique_id=unique)
            return render(request,"zarinpal/vocher.html", {
                'vochers': vochers
                })

        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')
