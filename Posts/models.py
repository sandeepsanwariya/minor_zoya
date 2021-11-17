from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.auth.models import User
from General.models import *
import datetime


class TextContent(models.Model):
    Id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Feature_Image = models.ImageField(upload_to='article-post')
    Headline = models.CharField(max_length=50)
    #wysiwyg_editor = Research
    Description = models.CharField(max_length=200,null=True)
    Content=models.TextField(default="<h1>Not Added Yet</h1>")
    fileid = models.CharField(max_length=100, null=True)
    Is_free = models.BooleanField(default=True)
    Created_on = models.DateTimeField(default=datetime.datetime.now)
    Updated_on = models.DateTimeField(default=datetime.datetime.now)
    Owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    Published=models.BooleanField(default=False)
    Like_count = models.IntegerField(default=0)
    def __str__(self): 
         return str(self.User)

class ImageContent(models.Model):
    Id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Headline = models.CharField(max_length=50)
    Image = models.URLField()
    fileid=models.CharField(max_length=100,null=True)
    Description = models.TextField()
    Is_free = models.BooleanField(default=True)
    Created_on = models.DateTimeField(default=datetime.datetime.now)
    Updated_on = models.DateTimeField(default=datetime.datetime.now)
    Published=models.BooleanField(default=False)
    Owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    Like_count = models.IntegerField(default=0)
    def __str__(self): 
         return str(self.User)
class VideoContent(models.Model):
    Id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Link = models.URLField(max_length=600)
    Title = models.CharField(max_length=500)
    fileid = models.CharField(max_length=100, null=True)
    Thumbnail = models.URLField()
    Description = models.TextField(default="No Description Available")
    Is_free = models.BooleanField(default=True)
    Published=models.BooleanField(default=False)
    Created_on = models.DateTimeField(default=datetime.datetime.now)
    Updated_on = models.DateTimeField(default=datetime.datetime.now)
    Owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    Like_count = models.IntegerField(default=0)
    def __str__(self): 
         return str(self.User)
     
class Notification(models.Model):
    Id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Send_to = models.ManyToManyField(User,related_name="send_to",blank=True)
    Message = models.TextField(default="No Messsage Available")
    Link=models.CharField(max_length=100,default="/")
    
class ImageTrace(models.Model):
    Id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    User=models.ForeignKey(User, on_delete=models.CASCADE)
    Last_Image_Upload=models.CharField(max_length=500,default="")
    fileid = models.CharField(max_length=100, null=True)
    Current_Image=models.CharField(max_length=500,default="")
    type=models.CharField(max_length=500,default="")
