import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import hashlib

from django.shortcuts import render, redirect,HttpResponse,get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse
import requests



# Encryption Key and API URLs
ENCRYPTION_KEY = "E-m!tr@2016".ljust(16, '0').encode('utf-8')
IV = ENCRYPTION_KEY[:16]
BACK_TO_BACK_URL = "http://emitrauat.rajasthan.gov.in/webServicesRepositoryUat/backtobackTransactionWithEncryptionA"
VERIFICATION_URL = "http://emitrauat.rajasthan.gov.in/webServicesRepositoryUat/getTokenVerifyNewProcessByRequestIdWithEncryption"



def payment_page(request):
    """Render the payment form."""
    return render(request, 'payment_emitra.html')


# Utility functions for encryption and checksum
def encrypt_aes(data):
    cipher = Cipher(algorithms.AES(ENCRYPTION_KEY), modes.CBC(IV))
    encryptor = cipher.encryptor()
    padded_data = data + (16 - len(data) % 16) * chr(16 - len(data) % 16)
    encrypted = encryptor.update(padded_data.encode('utf-8')) + encryptor.finalize()
    return base64.b64encode(encrypted).decode('utf-8')

def calculate_checksum(params):
    sorted_params = sorted(params.items())
    checksum_str = ''.join([str(value) for _, value in sorted_params])
    return hashlib.md5(checksum_str.encode('utf-8')).hexdigest()

# Payment initiation view
def initiate_payment(request):
    """Initiate payment request."""
    request_data = {
        "MERCHANTCODE": "RISLTEST",
        "REQUESTID": "TXN12345",
        "REQTIMESTAMP": "20231209120000",
        "SERVICEID": "7095",
        "REVENUEHEAD": "863-3000.00|865-10.00",
        "CONSUMERKEY": "User12345",
        "CONSUMERNAME": "John Doe",
        "COMMTYPE": "3",
        "SSOID": "testKioskSSOID",
        "OFFICECODE": "RISLTESTHQ",
    }
    request_data["CHECKSUM"] = calculate_checksum(request_data)
    encrypted_data = encrypt_aes(str(request_data).replace("'", '"'))

    # Send the request
    response = requests.post(BACK_TO_BACK_URL, data={"encData": encrypted_data})

    # Debugging logs
    print("Response Status Code:", response.status_code)
    print("Encrypted Data Sent:", encrypted_data)
    print("Response Text:", response.text)
    print("Response Headers:", response.headers)

    # Handle the response
    if not response.text:
        return JsonResponse({
            "status": "error",
            "message": "API responded with status 200 but no content. Please check the API server."
        }, status=500)

    try:
        response_data = response.json()
        return JsonResponse({"status": "success", "data": response_data})
    except requests.exceptions.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Response not in JSON format", "raw_response": response.text}, status=response.status_code)


# Payment verification view
def verify_payment(request, transaction_id):
    """Verify a transaction status."""
    verification_data = {
        "MERCHANTCODE": "RISLTEST",
        "SERVICEID": "7095",
        "REQUESTID": transaction_id,
    }
    verification_data["CHECKSUM"] = calculate_checksum(verification_data)
    encrypted_data = encrypt_aes(str(verification_data).replace("'", '"'))
    
    response = requests.post(VERIFICATION_URL, data={"encData": encrypted_data})
    if response.status_code == 200:
        response_data = response.json()
        return render(request, 'payment_status.html', {
            "message": "Payment Verified Successfully",
            "transaction_id": response_data.get("TRANSACTIONID"),
            "status": response_data.get("TRANSACTIONSTATUS"),
        })
    return render(request, 'payment_status.html', {
        "message": "Payment Verification Failed",
        "transaction_id": transaction_id,
        "status": "FAILED",
    })

