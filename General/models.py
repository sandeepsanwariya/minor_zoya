from django.db import models
from django.conf import settings
from django.shortcuts import reverse
import uuid
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
import datetime



class Profile(models.Model):
    # blank=True, null=True remove? name gender?
    Id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Name = models.CharField(max_length=50, blank=True, null=True)
    username=models.CharField(max_length=100, blank=True, null=True)
    Gender = models.CharField(max_length=30, blank=True, null=True)
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    URL=models.URLField(max_length=200 ,null=True)
    Country= models.CharField(max_length=100, blank=True, null=True)
    UserType = models.CharField(max_length=100, blank=True, null=True)
    Account_activated = models.BooleanField(default=False)
    Profile_incomplete=models.BooleanField(default=True)
    DateOfBirth = models.DateField(max_length=8)
    Created_on = models.DateTimeField(auto_now_add=True)
    Avatar = models.CharField(max_length=100)
    fileid = models.CharField(max_length=100, null=True)
    Phone_no=models.CharField(max_length=20)
    Updated_on = models.DateTimeField(auto_now=True)
    tab_order=models.TextField(max_length=100,blank=True, null=True)
    Bio = models.TextField(default='No Bio')
    Profile_incomplete=models.BooleanField(default=True)
    Following = models.ManyToManyField(User,related_name="followers",blank=True) 
    Subscribed = models.ManyToManyField(User,related_name="subscribers",blank=True) 
    My_subscribers = models.ManyToManyField(User,related_name="my_subscribers",blank=True) 
    my_followers = models.ManyToManyField(User,related_name="my_followers",blank=True)
    otp_for_email=models.IntegerField(default=0,null=True) 
    otp_for_number=models.IntegerField(default=0,null=True)

    total_donations = models.FloatField(default=0.0,blank=True, null=True)
    Subscription_price = models.FloatField(default=0.0,null=True)
    Payment_ID = models.CharField(max_length=50,null=True)
    Revenue = models.FloatField(default=0.0,blank=True,null=True)

    Why_to_subscribe=models.TextField(default="") #Headline Where Creator can define 
    
    def __str__(self): 
         return str(self.user)
       

class Likes(models.Model):
    Id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Like_by=models.ForeignKey("Profile", related_name='Like_by', on_delete=models.CASCADE)
    Like_To=models.ForeignKey("Profile", related_name='Like_To', on_delete=models.CASCADE)
    Post_id= models.CharField(max_length=100)
    type=models.CharField(max_length=100,null=True)

class Bulletins(models.Model):#Used To Describe There Service Eficiently through Bullet Poinst  
  profile=models.ForeignKey( "Profile",null=True, on_delete=models.CASCADE) #? ADDED NEW 
  Content=models.TextField(blank=True,null=True)

class ShippingAddress(models.Model):
    Id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    User= models.OneToOneField(User, on_delete=models.CASCADE)
    address_line=models.TextField(default="")
    city=models.CharField(max_length=200,default="")
    state=models.CharField(max_length=200,default="")
    pin_code=models.CharField(max_length=200,default="")
    

class ImageTrack(models.Model):
    Id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    User= models.ForeignKey(User, on_delete=models.CASCADE)
    LastImageUploaded=models.CharField(max_length=1000)
    CurrentImage=models.CharField(max_length=1000)
  
class BankDetail(models.Model):
    Id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    Account_Number= models.CharField(max_length=100)
    IFSC_Code= models.CharField(max_length=100)
    Account_holder_name= models.CharField(max_length=100)
    Street_Address= models.CharField(max_length=200)
    City= models.CharField(max_length=100)
    State= models.CharField(max_length=100)
    Pincode= models.CharField(max_length=50)

    def __str__(self):
      return f'{self.user} - {self.Account_Number}'

class SocialMediaAccounts(models.Model):
    Id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    YouTube=models.CharField(max_length=200,blank=True,null=True)
    Instagram=models.CharField(max_length=200,blank=True,null=True)
    Facebook=models.CharField(max_length=200,blank=True,null=True)
    Twitter=models.CharField(max_length=200,blank=True,null=True)
    LinkedIn=models.CharField(max_length=200,blank=True,null=True)
    Takatak=models.CharField(max_length=200,blank=True,null=True)

    def __str__(self):
      return f'{self.user} - {self.user}'

class AmountRedeemed(models.Model):
        Id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        Amount=models.FloatField(default=0)
        Date=models.DateField()
        User=models.ForeignKey(User,on_delete=models.CASCADE)


