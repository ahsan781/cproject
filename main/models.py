from django.db import models
from django.contrib.auth.models import  AbstractUser
from django.contrib.auth.models import User
import uuid
from django.urls import reverse
from timezone_field import TimeZoneField
from datetime import datetime
import copy


class User(AbstractUser):
    username = models.CharField(max_length = 15,unique=True)
    first_name = models.CharField(max_length = 15)
    last_name = models.CharField(max_length = 15)
    email = models.EmailField()
    is_vendor = models.BooleanField(default=False)
  


class VendorProfile(models.Model):
    user =     models.OneToOneField(User,on_delete=models.CASCADE)
    name =     models.CharField(max_length = 30)

    def __str__(self):
        return self.user.username   
        

class MemberProfile(models.Model):
    vendor_profile =     models.ForeignKey(VendorProfile,on_delete=models.CASCADE,related_name='members')
    name           =     models.CharField(max_length =30)
    email          =     models.EmailField()


    def __str__(self):
        return self.name 


class CustomerProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='customer_profile')
    first_name =  models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)

    def __str__(self):
        return f'{self.first_name}{self.last_name}'



CAT = (
    ("admin","admin"),
    ("mobile","mobile"),
    ("archived","archived"),
   
)
job = (
    ("Customer 1","Customer 1"),
    ("Project A","Project A"),
    ("Shift Manager","Shift Manager"),
    ("Work site A","Work site A"),
   
)




class ShiftDetail(models.Model):
    user   =         models.ForeignKey(MemberProfile, on_delete=models.CASCADE,null=True,blank=True)
    title           = models.CharField(max_length=200,null=True)
    date            = models.DateField(null=True)
    start_time      = models.TimeField(null=True)
    end_time        = models.TimeField(null=True)
    created_date    = models.DateTimeField(auto_now_add=True,null=True)
    location        = models.CharField(max_length=200,null=True)
    note            = models.FileField(upload_to ='uploads/',null=True)
    job             = models.CharField(choices=job,max_length=50,null=True)
    tz1             = TimeZoneField(default='Asia/Calcutta',null=True,blank=True) 
    username        = models.CharField(max_length=200,null=True)
    text            = models.CharField(max_length=1000,null=True)
    

    def __str__(self):
        return self.title
    
    @property
    def get_html_url(self):
        # we are returning title in calendar home page
        return f' {self.title} '


class Template(models.Model):
    user             =models.ForeignKey(MemberProfile, on_delete=models.CASCADE,null=True,blank=True)
    title1           = models.CharField(max_length=200,null=True)
    date1            = models.DateField()
    start_time1      = models.TimeField(null=True)
    end_time1        = models.TimeField(null=True)
    location1        = models.CharField(max_length=200,null=True)
    tz11             = TimeZoneField(default='Asia/Calcutta',null=True,blank=True) 
    username1        = models.CharField(max_length=200,null=True)
    note            = models.FileField(upload_to ='uploads/',null=True)
    text1            = models.CharField(max_length=1000,null=True)

    def __str__(self):
        return self.title1
    
    @property
    def get_html_url(self):
        # we are returning title in calendar home page
        return f' {self.title1} '




class AddUser(models.Model):
    first_name = models.CharField(max_length =255)
    last_name = models.CharField(max_length =255)
    email = models.EmailField(null=True ,max_length=255)
    mobile =  models.CharField(max_length=255)

    def __str__(self):
        return self.first_name
    




class EventMember(models.Model):
    event = models.ForeignKey(ShiftDetail, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['event', 'user']

    def __str__(self):
        return str(self.user)



class MultiduplicateTask(models.Model):
    numbers = models.IntegerField(default=2)


    