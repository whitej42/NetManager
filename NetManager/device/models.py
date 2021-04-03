from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# device object
class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=False)
    type = models.CharField(max_length=250, null=False)
    host = models.CharField(max_length=250, null=False)
    vendor = models.CharField(max_length=250, null=False)
    location = models.CharField(max_length=250, default='Not Specified')
    contact = models.CharField(max_length=250, default='Not Specified')
    username = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    secret = models.CharField(max_length=250)
    status = models.BooleanField(default=False, editable=False)


# config log object
class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.CharField(max_length=250, null=False)
    type = models.CharField(max_length=250, null=False)
    description = models.CharField(max_length=250, null=False)
    date = models.DateField(default=timezone.now().date())
    time = models.TimeField(default=timezone.now().time())
    flag = models.BooleanField(default=False)