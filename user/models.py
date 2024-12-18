from django.db import models
from django.utils import timezone
from datetime import datetime, date
from django.contrib.auth.models import User
import os

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    tel = models.CharField(max_length=10)
    state = models.CharField(max_length=30) 
    city = models.CharField(max_length=30)
    pincode = models.CharField(max_length=30)
    msg = models.TextField()
    def __str__(self):
        objName = f"{self.name} {self.pincode} {date.today()}"
        return objName
    
# class InfoAPI(models.Model):
#     merchantID = models.CharField(max_length=50)
#     SSOID = models.CharField(max_length=50)
#     USERNAME = models.CharField(max_length=100)
#     def __str__(self):
#         objName = f"{self.merchantID} {self.SSOID} {self.USERNAME} {date.today()}"
#         return objName

class Advertisement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='advertisements/', blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=20, unique=True)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency_code = models.CharField(max_length=3, default='INR')
    status = models.CharField(max_length=20, default='Pending')  # Pending, Success, or Failed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.order_id} - {self.status}"

class InfoAPI(models.Model):
    ssoid = models.CharField(max_length=30)
    merchantid = models.CharField(max_length=30)
    username = models.CharField(max_length=100)
    def __str__(self):
        objName = f"{self.merchantid} {self.ssoid} {self.username} {date.today()}"
        return objName


# #Special Login
# class UserProfile(models.Model):
#     ssoid = models.CharField(max_length=100, unique=True)
#     merchantid = models.CharField(max_length=100, unique=True)

#     def __str__(self):
#         return self.ssoid


class Location(models.Model):
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.district}, {self.state}"

class UserForm(models.Model):
    user_state = models.CharField(max_length=100,null=True,blank=True)
    district = models.CharField(max_length=100,null=True,blank=True)
    fullName = models.CharField(max_length=100,null=True,blank=True)
    fatherName = models.CharField(max_length=100,null=True,blank=True)
    motherName = models.CharField(max_length=100,null=True,blank=True)
    dob = models.CharField(max_length=100,null=True,blank=True)
    category = models.CharField(max_length=100,null=True,blank=True)
    gender = models.CharField(max_length=100,null=True,blank=True)
    nationality = models.CharField(max_length=100,null=True,blank=True)
    marital = models.CharField(max_length=100,null=True,blank=True)
    disability = models.CharField(max_length=100,null=True,blank=True)
    select_disability = models.CharField(max_length=100,null=True,blank=True)
    dsrvs = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    userstate = models.CharField(max_length=100,null=True,blank=True)
    userdistrict = models.CharField(max_length=100,null=True,blank=True)
    pin_code = models.CharField(max_length=100,null=True,blank=True)
    phone = models.CharField(max_length=100,null=True,blank=True)
    mobile = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    passing_year = models.CharField(max_length=100,null=True,blank=True)
    diviosn_grade = models.CharField(max_length=100,null=True,blank=True)
    secondary_passing_year = models.CharField(max_length=100,null=True,blank=True)
    secondary_passing_grade = models.CharField(max_length=100,null=True,blank=True)
    higher_secondary_passing_year = models.CharField(max_length=100,null=True,blank=True)
    higher_secondary_passing_grade = models.CharField(max_length=100,null=True,blank=True)
    graduate_passing_year = models.CharField(max_length=100,null=True,blank=True)
    graduate_passing_grade = models.CharField(max_length=100,null=True,blank=True)
    post_graduate_passing_year = models.CharField(max_length=100,null=True,blank=True)
    post_graduate_passing_grade = models.CharField(max_length=100,null=True,blank=True)
    professional_passing_year = models.CharField(max_length=100,null=True,blank=True)
    professional_passing_grade = models.CharField(max_length=100,null=True,blank=True)
    id_proof_select = models.CharField(max_length=100,null=True,blank=True)
    id_proof_number = models.CharField(max_length=100,null=True,blank=True)
    id_proof_marks = models.CharField(max_length=100,null=True,blank=True)
    id_proof_study_center = models.CharField(max_length=100,null=True,blank=True)
    id_proof_school = models.CharField(max_length=100,null=True,blank=True)
    i_agree = models.CharField(max_length=100,null=True,blank=True)
    passport_size_photo = models.ImageField(upload_to="userform/",null=True,blank=True)
    signature = models.ImageField(upload_to="userform/",null=True,blank=True)
    captcha_code = models.CharField(max_length=100,null=True,blank=True)
    place = models.CharField(max_length=100,null=True,blank=True)
    dated = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return f"{self.fullName}, {self.phone}"

def custom_image_upload_path(instance, filename):
    # Split the filename to get the file extension
    ext = filename.split('.')[-1]
    # Create a new filename with instance ID and current timestamp
    new_filename = f"{instance.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
    # Return the full upload path
    return os.path.join('photos/', new_filename)

# class Profile(models.Model):
#     passport_size_photo = models.ImageField(upload_to=custom_image_upload_path)

#     def save(self, *args, **kwargs):
#         if not self.id:
#             # Save once to get the instance ID if it’s a new instance
#             super(Profile, self).save(*args, **kwargs)
#         # Use the custom path function for naming
#         self.passport_size_photo.name = custom_image_upload_path(self, self.passport_size_photo.name)
#         super(Profile, self).save(*args, **kwargs)


# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField(blank=True)
#     location = models.CharField(max_length=100, blank=True)

#     def __str__(self):
#         return self.user.username