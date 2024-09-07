from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User

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
        objName = f"{self.name} {self.pincode} {datetime.date.today()}"
        return objName
    
class InfoAPI(models.Model):
    merchantID = models.CharField(max_length=50)
    SSOID = models.CharField(max_length=50)
    def __str__(self):
        objName = f"{self.merchantID} {self.SSOID} {datetime.date.today()}"
        return objName


# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField(blank=True)
#     location = models.CharField(max_length=100, blank=True)

#     def __str__(self):
#         return self.user.username