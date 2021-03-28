from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


# device object
class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deviceName = models.CharField(max_length=250, null=False)
    deviceType = models.CharField(max_length=250, null=False)
    host = models.CharField(max_length=250, null=False)
    vendor = models.CharField(max_length=250, null=False)
    location = models.CharField(max_length=250, default='Not Specified')
    contact = models.CharField(max_length=250, default='Not Specified')
    username = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    secret = models.CharField(max_length=250)
    status = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return self.deviceName


# config log object
class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.CharField(max_length=250, null=False)
    type = models.CharField(max_length=250, null=False)
    description = models.CharField(max_length=250, null=False)
    dateTime = models.DateTimeField(default=datetime.now())
    flag = models.BooleanField(default=False)
