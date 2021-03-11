import random

from django.db import models
from datetime import datetime
import random


# device object
class Device(models.Model):
    device = models.CharField(primary_key=True, max_length=250, null=False)
    deviceType = models.CharField(max_length=250, null=False)
    host = models.CharField(max_length=250, null=False)
    vendor = models.CharField(max_length=250, null=False)
    location = models.CharField(max_length=250, default='Not Specified')
    contact = models.CharField(max_length=250, default='Not Specified')
    status = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return self.device


# config log object
class Log(models.Model):
    id = models.AutoField(primary_key=True, max_length=6, null=False)
    device = models.CharField(max_length=250, null=False)
    user = models.CharField(max_length=250, null=False)
    type = models.CharField(max_length=250, null=False)
    description = models.CharField(max_length=250, null=False)
    dateTime = models.DateTimeField(default=datetime.now)
    flag = models.BooleanField(default=False)
