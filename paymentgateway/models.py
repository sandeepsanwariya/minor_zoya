from django.db import models
from General.models import Profile
import uuid
import datetime
# Create your models here.
class Plan(models.Model):
    Id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    planName=models.CharField(max_length=100)
    period=models.CharField(max_length=100)
    interval=models.IntegerField(default=1)
    amount=models.IntegerField(default=0)
    description=models.TextField(default=" ")
    planId=models.CharField(max_length=100,default="")
    
    def __str__(self): 
         return str(self.planName)
     
class Subscriptions(models.Model):
     Id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
     Customer_profile=models.ForeignKey(Profile,related_name="customer_subscription",on_delete=models.CASCADE,null=True)
     Creator_profile=models.ForeignKey(Profile,related_name="creator_subscription",on_delete=models.CASCADE,null=True)
     amount=models.FloatField()
     subscriptionId=models.CharField(max_length=200,unique=True,default="")
     subscriptionLink=models.CharField(max_length=200,unique=True,default="")
     planId=models.CharField(max_length=500,default="",null=True)
     status=models.CharField(max_length=100,default="not created")
     cancelled=models.BooleanField(default=False)


class Donations(models.Model):
    Id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Customer_profile = models.ForeignKey(Profile, related_name="customer_donation", on_delete=models.CASCADE,null=True)
    Creator_profile = models.ForeignKey(Profile, related_name="creator_donation", on_delete=models.CASCADE,null=True)
    amount = models.FloatField()
    order_id = models.CharField(max_length=200, unique=True, null=True)
    payment_id = models.CharField(max_length=200, unique=True, null=True)
    signature= models.CharField(max_length=500, null=True)
    status = models.CharField(max_length=100, default="not created")
    cancelled = models.BooleanField(default=False)
     
class ProductPurchased(models.Model):
     Id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
     Customer_profile=models.ForeignKey(Profile,related_name="customer",on_delete=models.CASCADE,null=True)
     Creator_profile=models.ForeignKey(Profile,related_name="creator",on_delete=models.CASCADE,null=True)
     linkRefrence_id=models.CharField(max_length=100,default="")
     payment_id=models.CharField(max_length=100,default="")
     link_id=models.CharField(max_length=100,default="")
     status=models.CharField(max_length=100,default="")
     amount=models.FloatField(default=0)

     
     
  