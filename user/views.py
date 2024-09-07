import requests
from datetime import datetime
from .utils import generate_checksum  # Assuming the checksum utility is in utils.py
from user import models
from django.shortcuts import render, redirect,HttpResponse
from django.conf import settings
from django.contrib.auth import login, authenticate
from .forms import SignUpForm

from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

from django.http import JsonResponse
import zlib
import requests
from requests.auth import HTTPBasicAuth
import json
from .forms import TransactionForm

from django.core.mail import send_mail


# Create your views here.

def send_email(request,email):
        recipient_list = [email]
        send_mail(
            subject='This is from django',
            message='Hello World.',
            from_email='emitraapi@gmail.com',
            recipient_list=recipient_list,
            fail_silently=False,
)
        return HttpResponse("Email Sent! Successfully")


# Generate checksum
def generate_checksum(message, secret_key):
    msg = message + "|" + secret_key
    bytes_data = msg.encode('utf-8')
    checksum_value = zlib.crc32(bytes_data)
    return checksum_value

# Initiate Transaction View
def initiate_transaction(request):
    messageType = ""
    merchantId = "UATIDEEDSG0000001536"
    serviceId = "IDEED03"
    orderId = ""
    customerId = ""
    transactionAmount = 250
    currencyCode = "INR"
    requestDateTime = ""
    successUrl = "https://www.google.com"
    failUrl = "https://www.instagram.com"

    message = f"{messageType}|{merchantId}|{serviceId}|{orderId}|{customerId}|{transactionAmount}|{currencyCode}|{requestDateTime}|{successUrl}|{failUrl}"

    secret_key = "2cf0f5d878e83150c5d36b0b07b737db8636e259046ac4b05baa7deeb8712eed"
    data = {"RequestAPI":generate_checksum(message,secret_key)}
    return render(request, 'initiate_transaction.html',data)

# Transaction Status View
def transaction_status(request):
    mid = request.GET.get('mid')
    order_id = request.GET.get('order_id')
    username = "your_username"
    password = "your_password"
    url = f"https://surepay.ndml.in/SurePayPayment/v1/queryPaymentStatus?requestMsg=|{mid}|{order_id}"
    response = requests.post(url, auth=HTTPBasicAuth(username, password))
    return JsonResponse(response.json())

def payment_sucess(request):
    return HttpResponse("Payment Successul!")

def payment_fail(request):
    return HttpResponse("Payment Failed!")

# Refund Transaction View
def refund_transaction(request):
    if request.method == 'POST':
        data = request.POST
        url = "https://surepay.ndml.in/SurePayPayment/refundTransaction"
        payload = json.dumps({
            "refundApiRequest": [
                {
                    "surePayMerchantId": data['mid'],
                    "orderId": data['order_id'],
                    "refundReqId": data['refund_req_id'],
                    "bankTransactionNo": data['bank_transaction_no'],
                    "serviceId": data['service_id'],
                    "surePayTxnId": data['surepay_txn_id'],
                    "transactionAmount": data['transaction_amount'],
                    "refAmount": data['ref_amount'],
                    "checkSum": data['checksum']
                }
            ]
        })
        headers = {
            'Authorization': HTTPBasicAuth("your_username", "your_password"),
            'Content-Type': 'application/json',
        }
        response = requests.post(url, headers=headers, data=payload)
        return JsonResponse(response.json())
    return render(request, 'refund_transaction.html')

def list_to_dict(lst):
    res_dict = {}
    for i in range(0, len(lst), 2):
        res_dict[lst[i]] = lst[i + 1]
    return res_dict


def index(request):

    try:
        users = models.InfoAPI.objects.all()
        for user in users:
            pass
        
        url = "http://emitrauat.rajasthan.gov.in/webServicesRepositoryUat/getKioskDetailsJSON"
        payload = {
        "MERCHANTCODE": user.merchantID,
        "SSOID": user.SSOID,
        }

        headers = {
        "Content-Type": "application/x-www-form-urlencoded"
        }
        
        if request.method == "POST":
            merchantID = request.POST.get("merchantID")
            SSOID = request.POST.get("SSOID")
            ins = models.InfoAPI(merchantID=merchantID,SSOID=SSOID)
            ins.save()
            print(1)
        else:
            print("Failed to Fetch the details")

        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            # arguments = list(response.json().items())  

            text = {"keys":response.json(),
                    "values":response.json().values()
                    }

        else:
            print("Failed to get a response")
            print("Status code:", response.status_code)
            print("Response text:", response.text)
            text = {"t1":"Error 404 please contact your admin"}
    except Exception as e:
        print("Please Check your internet connection")

    return render(request,"index.html",text)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def about(request):
    return render(request,"about.html")

def contact(request):
    if request.method == 'POST':

        name = request.POST.get("name")
        email = request.POST.get("email")
        tel = request.POST.get("tel")
        state = request.POST.get('state')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        msg = request.POST.get("message")
        ins = models.Contact(name=name,email=email,tel=tel,state=state,city=city,pincode=pincode,msg=msg)
        ins.save()
        print("The data has been written to the database")
        

    return render(request,"contact.html")
 
def services(request):
    return render(request,"services.html")

def applications(request):
    return render(request,"applications.html")

def donations(request):
    return render(request,'donations.html')

def newbranch(request):
    return render(request, 'newbranch.html')

def payment_page(request):
    return render(request,"query_payment_status.html")



