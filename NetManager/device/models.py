from django.db import models
from datetime import datetime


# config log object - MOVE THIS!!
class Log(models.Model):
    device = models.CharField(max_length=250, null=False)
    user = models.CharField(max_length=250, null=False)
    type = models.CharField(max_length=250, null=False)
    description = models.CharField(max_length=250, null=False)
    dateTime = models.DateTimeField(default=datetime.now)
    flag = models.BooleanField(default=False)
