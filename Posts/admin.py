from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(ImageContent)
admin.site.register(TextContent)
admin.site.register(VideoContent)
admin.site.register(Notification)
admin.site.register(ImageTrace)
admin.site.register(Likes)

