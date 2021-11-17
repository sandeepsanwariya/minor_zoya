from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.auth.models import User
from General.models import *
import datetime

class StoreItem(models.Model):
    Id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    Owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    Image = models.ImageField()
    Headline = models.CharField(max_length=50)
    Description =  models.TextField()
    Price = models.FloatField()
    Published=models.BooleanField(default=False)
    Created_on = models.DateTimeField(default=datetime.datetime.now)
    Updated_on = models.DateTimeField(default=datetime.datetime.now)
    Like_count = models.IntegerField(default=0)
