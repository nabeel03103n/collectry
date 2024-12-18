from reportlab.lib.pagesizes import letter
from django.contrib.auth.models import User
from reportlab.pdfgen import canvas
import requests
from django.contrib.auth.decorators import login_required,user_passes_test
from .utils import generate_checksum  # Assuming the checksum utility is in utils.py
from user import models
from django.shortcuts import render, redirect,HttpResponse,get_object_or_404
from django.conf import settings
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from datetime import datetime
import random
from django.http import JsonResponse
import zlib
import requests
from requests.auth import HTTPBasicAuth
import json
from .forms import AdvertisementForm

from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt







# Create your views here.

def get_emitra_api_response(ssoid, merchantid):
    """
    This function makes a request to the Emitra API using the provided ssoid and merchantid.
    Returns the response data if successful, otherwise returns an error message.
    """
    url = "http://emitrauat.rajasthan.gov.in/webServicesRepositoryUat/getKioskDetailsJSON"
    payload = {
        "MERCHANTCODE": merchantid,
        "SSOID": ssoid,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        # Send POST request to the Emitra API
        response = requests.post(url, data=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            data_keys = list(data.keys())
            data_values = list(data.values())
            return {"keys": data_keys, "values": data_values, "data": zip(data_keys, data_values)}
        else:
            return {"error": f"API response error: {response.status_code}, {response.text}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while fetching data: {e}"}


def index(request):
    text = {"t1": "No data available"}
    try:
        current_user = request.user  # Get the currently logged-in user
        
        # Check if the user is authenticated
        if not current_user.is_authenticated:
            raise ValueError("User is not logged in or authenticated.")

        # Retrieve user-specific data from the database
        user = models.InfoAPI.objects.filter(username=current_user.username).last()
        if not user:
            raise ValueError(f"No data available for the user: {current_user.username}")

        # Prepare API request
        url = "http://emitrauat.rajasthan.gov.in/webServicesRepositoryUat/getKioskDetailsJSON"
        payload = {
            "MERCHANTCODE": user.merchantid,
            "SSOID": user.ssoid,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        # Send POST request to the API
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            data_keys = list(response.json().keys())
            data_values = list(response.json().values())
            data = zip(data_keys, data_values)

            text = {"keys": data_keys, "values": data_values, "data": data}
        else:
            print(f"API response error: {response.status_code}, {response.text}")
            text = {"t1": "Error fetching API details, please contact your admin"}
    except Exception as e:
        print(f"An exception occurred: {e}")
        return render(request, "index_failed.html", text)

    return render(request, "index.html", text)




def send_email(request,email,subject,message):
        recipient_list = [email]
        send_mail(
            subject=subject,
            message=message,
            from_email='emitraapi@gmail.com',
            recipient_list=recipient_list,
            fail_silently=False,
)
        return "Message Sent! Successfully"

def generate_checksum(message, secret_key):
    msg = message + "|" + secret_key
    bytes_data = msg.encode('utf-8')
    checksum_value = zlib.crc32(bytes_data) & 0xffffffff  # Ensure checksum is unsigned
    return checksum_value

def query_transaction_status(merchant_id, order_id, bank_reference_id=None):

    username = "UATIDEEDSG0000001536"  # Replace with actual username
    password = "jtuamnwsggmkknstwycz"

    base_url = "https://pilot.surepay.ndml.in/SurePayPayment/v1/queryPaymentStatus"  # UAT URL

    # Construct the request message
    if bank_reference_id:
        request_msg = f"{bank_reference_id}|{merchant_id}|{order_id}"
    else:
        request_msg = f"|{merchant_id}|{order_id}"

    payload = {'requestMsg': request_msg}

    try:
        # Send the POST request
        response = requests.post(
            base_url,
            data=payload,
            auth=HTTPBasicAuth(username.strip(), password.strip())
        )

        # Debugging output for troubleshooting
        print(f"Request sent to {base_url}")
        print(f"Payload: {payload}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        # Check if response is plain text
        if response.status_code == 200:
            # Return raw text response for further processing
            return {"status": "success", "response": response.text}
        else:
            # Handle unsuccessful status codes
            return {"error": f"HTTP {response.status_code}", "details": response.text}
    except Exception as e:
        return {"error": "Exception occurred", "details": str(e)}


#Emitra API (payment)
# from . import emitra_api

# Sure Pay API (payment)
orderId = ""
transactionAmount = 0
merchantId = ""
# Initiate Transaction View
@csrf_exempt
def initiate_transaction(request):
    global merchantId
    global orderId
    global transaction_amount
    if request.method == 'POST':
        # Retrieve posted data
        messageType = request.POST.get('messageType')
        merchantId = request.POST.get('merchantId')
        serviceId = request.POST.get('serviceId')
        orderId = str(random.randint(88055, 188055))
        # orderId = request.POST.get('orderId')
        customerId = request.POST.get('customerId')
        transactionAmount = request.POST.get('transactionAmount')
        currencyCode = request.POST.get('currencyCode')
        requestDateTime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        successUrl = request.POST.get('successUrl')
        failUrl = request.POST.get('failUrl')
        additionalField1 = request.POST.get('additionalField1', '')
        additionalField2 = request.POST.get('additionalField2', '')
        additionalField3 = request.POST.get('additionalField3', '')
        additionalField4 = request.POST.get('additionalField4', '')
        additionalField5 = request.POST.get('additionalField5', '')

        user = request.user  # Assumes user is authenticated
        transaction_amount = request.POST.get('transactionAmount')

        # # Create or retrieve a Payment record for this transaction
        # payment, created = models.Payment.objects.get_or_create(
        #     user=user,
        #     order_id=orderId,
        #     defaults={'transaction_amount': transaction_amount, 'status': 'Pending'}
        # )

        # Construct message for checksum generation
        message = f"{messageType}|{merchantId}|{serviceId}|{orderId}|{customerId}|{transactionAmount}|{currencyCode}|{requestDateTime}|{successUrl}|{failUrl}|{additionalField1}|{additionalField2}|{additionalField3}|{additionalField4}|{additionalField5}"
        secret_key = "2cf0f5d878e83150c5d36b0b07b737db8636e259046ac4b05baa7deeb8712eed"
        checksum = generate_checksum(message, secret_key)

        # Data to be sent to the payment page
        data = {
            "messageType": messageType,
            "merchantId": merchantId,
            "serviceId": serviceId,
            "orderId": orderId,
            "customerId": customerId,
            "transactionAmount": transactionAmount,
            "currencyCode": currencyCode,
            "requestDateTime": requestDateTime,
            "successUrl": successUrl,
            "failUrl": failUrl,
            "additionalField1": additionalField1,
            "additionalField2": additionalField2,
            "additionalField3": additionalField3,
            "additionalField4": additionalField4,
            "additionalField5": additionalField5,
            "checksum": checksum
        }

        # Render a template that will auto-submit the data to SurePay's URL
        username = "UATIDEEDSG0000001536"  # Replace with actual username
        password = "jtuamnwsggmkknstwycz"  # Replace with actual password
        bank_reference_id = None  # Provide if available
        print(data)
        query_transaction_status(merchant_id=merchantId,order_id=orderId,username=username,password=password,bank_reference_id=bank_reference_id)
        return render(request, 'redirect_to_surepay.html', {'surepay_url': "https://pilot.surepay.ndml.in/SurePayPayment/sp/processRequest", 'data': data})
    

    return render(request, 'initiate_transaction.html')




def some_view(request):
    # Check if the user has completed a payment successfully
    payment_exists = models.Payment.objects.filter(user=request.user, status='Success').exists()

    if payment_exists:
        # User has a successful payment, so hide the payment option
        return render(request, 'no_payment_required.html')
    else:
        # No successful payment, proceed to show the payment option
        return render(request, 'initiate_transaction.html')



def payment_success(request):

    payment, created = models.Payment.objects.get_or_create(
            user=request.user,
            order_id=orderId,
            defaults={'transaction_amount': 250, 'status': query_transaction_status(merchantId,orderId)}
        )
    return HttpResponse("Payment Successul!")

def payment_fail(request):
    return HttpResponse("Payment Failed!")

def list_to_dict(lst):
    res_dict = {}
    for i in range(0, len(lst), 2):
        res_dict[lst[i]] = lst[i + 1]
    return res_dict


@login_required
def advertisement_list(request):
    advertisements = models.Advertisement.objects.all()
    return render(request, 'advertisements/advertisement_list.html', {'advertisements': advertisements})
# Helper function to check if the user is an admin
def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def add_advertisement(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('advertisement_list')
    else:
        form = AdvertisementForm()
    
    return redirect("http://127.0.0.1:8000/admin/user/advertisement/add/")
    # return render(request, 'advertisements/add_advertisement.html', {'form': form})


# def special_login(request):
#     # Get ssoid and merchantid parameters from the URL (or POST request)
#     ssoid = request.GET.get('ssoid')
#     merchantid = request.GET.get('merchantid')
#     response = get_emitra_api_response(ssoid,merchantid)
#     return HttpResponse(f"{response}")
    

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password1")


        print(f"{email} {username} {password}")
        

        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def about(request):
    return render(request,"about.html")

def home(request):
    advertisements = models.Advertisement.objects.all()

    return render(request,"home.html",{"advertisements":advertisements})

from reportlab.lib.units import inch
def create_pdf(filename, content, image_1_path=None,image_2_path=None):
    c = canvas.Canvas(filename, pagesize=letter)
    y = 750  # Starting y position for text
    c.setTitle("User Information")

    # Draw each line of content at a new position
    for line in content:
        c.drawString(100, y, line)  # Draw each line with horizontal positioning
        y -= 20  # Move down 20 units for each new line
    
    try:
        # If the image path is provided, draw the image
        if image_1_path and image_2_path:
            # Set the position where the image will be placed (X, Y) and the size of the image
            c.drawImage(image_1_path, 100, y - 100, width=1.5*inch, height=1.5*inch)  # Adjust the width and height as needed
            y -= 150
            c.drawImage(image_2_path, 100, y - 100, width=1.5*inch, height=1.5*inch)  # Adjust the width and height as needed
            y -= 150
    except IOError:
        print(f"Error: Could not open image {image_1_path or image_2_path}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    c.save()


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

        message = f"Name : {name}\nEmail : {email}\nPhone Number : {tel}\nState : {state}\nCity : {city}\nPincode : {pincode}\n\n{msg}"

        print("The data has been written to the database")
        return HttpResponse(send_email(request,email=email,subject=f"Contact form From - {tel}",message=message))

    return render(request,"contact.html")
 
def services(request):
    return render(request,"services.html")

def applications(request):
    return render(request,"applications.html")

def donations(request):
    return render(request,'donations.html')

def newbranch(request):
    return render(request, 'newbranch.html')

def termsAndCondition(request):
    return HttpResponse("This is termsAndCondition page")

def privacyPolicy(request):
    return HttpResponse("This is privacyPolicy page")

def GrievanceRedressalPolicy(request):
    return HttpResponse("This is GrievanceRedressalPolicy page")


# views.py

def form_page(request):
    # Get unique states and districts
    states = models.Location.objects.values_list("state", flat=True).distinct()
    states = [""] + list(states)  # Add an empty option at the beginning

    districts = []  # Start with an empty list for GET requests

    if request.method == 'POST':
        user_state = request.POST.get('state')
        user_data = {
            "user_state": user_state,
            "district": request.POST.get('district'),
            "fullName": request.POST.get('fullName'),
            "fatherName": request.POST.get("fatherName"),
            "motherName": request.POST.get("motherName"),
            "dob": request.POST.get("DOB"),
            "category": request.POST.get("category"),
            "gender": request.POST.get("gender"),
            "nationality": request.POST.get("nationality"),
            "marital": request.POST.get("marital"),
            "disability": request.POST.get("disability"),
            "select_disability": request.POST.get("select_disability"),
            "dsrvs": request.POST.get("DSRVS"),
            "address": request.POST.get("address"),
            "city": request.POST.get("city"),
            "userstate": request.POST.get("userstate"),
            "userdistrict": request.POST.get("userdistrict"),
            "pin_code": request.POST.get("pin_code"),
            "phone": request.POST.get("phone"),
            "mobile": request.POST.get("mobile"),
            "email": request.POST.get("email"),
            "passing_year": request.POST.get("passing_year"),
            "diviosn_grade": request.POST.get("diviosn_grade"),
            "secondary_passing_year": request.POST.get("secondary_passing_year"),
            "secondary_passing_grade": request.POST.get("secondary_passing_grade"),
            "higher_secondary_passing_year": request.POST.get("higher_secondary_passing_year"),
            "higher_secondary_passing_grade": request.POST.get("higher_secondary_passing_grade"),
            "graduate_passing_year": request.POST.get("graduate_passing_year"),
            "graduate_passing_grade": request.POST.get("graduate_passing_grade"),
            "post_graduate_passing_year": request.POST.get("post_graduate_passing_year"),
            "post_graduate_passing_grade": request.POST.get("post_graduate_passing_grade"),
            "professional_passing_year": request.POST.get("professional_passing_year"),
            "professional_passing_grade": request.POST.get("professional_passing_grade"),
            "id_proof_select": request.POST.get("id_proof_select"),
            "id_proof_number": request.POST.get("id_proof_number"),
            "id_proof_marks": request.POST.get("id_proof_marks"),
            "id_proof_study_center": request.POST.get("id_proof_study_center"),
            "id_proof_school": request.POST.get("id_proof_school"),
            "i_agree": request.POST.get("i_agree"),
            "captcha_code": request.POST.get("captcha_code"),
            "place" : request.POST.get("place_"),
            "dated": request.POST.get("dated"),
            "passport_size_photo": request.FILES.get("passport_size_photo"),
            "signature":request.FILES.get("signature"),

            # Add any other data you want to process or display
        }

        # Images Fields
        passport_size_photo = request.FILES.get("passport_size_photo")
        passport_size_photo_path = f"media/userform/{passport_size_photo}"

        signature = request.FILES.get("signature")
        signature_path = f"media/userform/{signature}"

        # Get districts based on the selected state for POST request
        district = models.Location.objects.filter(state=user_state).values_list('district', flat=True).distinct()
        districts = list(district)  # Convert queryset to list for rendering

        user_data_for_pdf = [f"{key}: {value}" for key, value in user_data.items() if value]
        create_pdf("static/pdf/output.pdf",user_data_for_pdf,passport_size_photo_path,signature_path)

        model = models.UserForm.objects.create(**user_data)

        return render(request, "form/form_submit.html", {"data": user_data})

    return render(request, "form/form.html", {"states": states, "districts": districts})


def get_districts(request):
    if request.method == "POST":
        state = request.POST.get('state')
        print(f"State received: {state}")  # Debugging line

        districts = models.Location.objects.filter(state=state).values_list('district', flat=True).distinct()
        print(f"Districts found: {districts}")  # Debugging line

        return JsonResponse({'districts': list(districts)})

    return JsonResponse({'districts': []})

