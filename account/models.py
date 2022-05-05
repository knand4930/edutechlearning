from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from datetime import datetime, timedelta, date
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
# Create your models here.
import datetime
from datetime import timedelta
from datetime import datetime as dt

today = datetime.date.today()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=1000)
    mobile = models.CharField(max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# @receiver(pre_save, sender=Profile)
# def update_active(sender, instance, *args, **kwargs):
#     if instance.pro_expire_date == today:
#         instance.paid = False
#     else:
#         instance.paid = True

#     def __str__(self):
#         return self.user.username

class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    sub = models.CharField(max_length=500)
    msg = models.TextField()
    
    def __str__(self):
        return self.name
    

class AboutUs(models.Model):
    name = models.CharField(max_length=300)
    short = models.CharField(max_length=600)
    desc = RichTextField()
    img = models.ImageField(upload_to='aboutus/')
    
    def __str__(self):
        return self.name