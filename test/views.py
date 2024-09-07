import requests
from django.views import View
from requests.auth import HTTPBasicAuth
from django.shortcuts import render
from user import models
from django.shortcuts import render
from django.http import JsonResponse
from requests.exceptions import ConnectionError, Timeout, HTTPError
import time
from django.shortcuts import render, redirect
from .nsdl_surepay import generate_checksum, process_payment_response
from django.conf import settings
from emitra.settings import MERCHANT_ID,SERVICE_ID,SECRET_KEY
import hashlib
import hmac
import base64

def make_payment_request(request):
    # Set up the payment request parameters
    message_type = '0100'
    merchant_id = MERCHANT_ID
    service_id = SERVICE_ID
    order_id = '123456'
    customer_id = '987654'
    transaction_amount = '100.00'
    currency_code = 'INR'
    request_datetime = '2023-03-22 10:30:00'
    success_url = 'https://127.0.0.1/success'
    fail_url = 'https://127.0.0.1/failure'
    additional_field1 = ''
    additional_field2 = ''
    additional_field3 = ''
    additional_field4 = ''
    additional_field5 = ''

    # Concatenate the parameters into a message string
    message = '|'.join([message_type, merchant_id, service_id, order_id, customer_id, transaction_amount, currency_code, request_datetime, success_url, fail_url, additional_field1, additional_field2, additional_field3, additional_field4, additional_field5])

    # Calculate the checksum using the HMAC-SHA256 algorithm
    secret_key = settings.SECRET_KEY.encode()
    message = message.encode()
    checksum = hmac.new(secret_key, message, hashlib.sha256).hexdigest()

    # Send the payment request to the NSDL SurePay API
    url = 'https://pilot.surepay.ndml.in/SurePayPayment/sp/processRequest'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'messageType': message_type,
        'merchantId': merchant_id,
        'serviceId': service_id,
        'orderId': order_id,
        'customerId': customer_id,
        'transactionAmount': transaction_amount,
        'currencyCode': currency_code,
        'requestDateTime': request_datetime,
        'successUrl': success_url,
        'failUrl': fail_url,
        'additionalField1': additional_field1,
        'additionalField2': additional_field2,
        'additionalField3': additional_field3,
        'additionalField4': additional_field4,
        'additionalField5': additional_field5,
        'checksum': checksum,
    }
    response = requests.post(url, headers=headers, data=data)

    # Process the response from the NSDL SurePay API
    if response.status_code == 200:
        # Handle a successful payment request
        return render(request, 'index.html')
    else:
        # Handle an error in the payment request
        pass

    return render(request, 'make_payment.html')