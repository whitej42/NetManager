"""

DEVICE MODELS.PY

"""

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=False)
    type = models.CharField(max_length=250, null=False)
    host = models.CharField(max_length=250, null=False)
    vendor = models.CharField(max_length=250, null=False)
    location = models.CharField(max_length=250, default='Not Specified')
    contact = models.CharField(max_length=250, default='Not Specified')
    status = models.BooleanField(default=False, editable=False)

    def get_device(self):
        device = Device.objects.get(pk=self)
        return device


class Security(models.Model):
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
    username = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    secret = models.CharField(max_length=250)

    def get_username(self):
        username = Security.objects.filter(device_id=self.id).get().username
        return username

    def get_password(self):
        password = Security.objects.filter(device_id=self.id).get().password
        return password

    def get_secret(self):
        secret = Security.objects.filter(device_id=self.id).get().secret
        return secret


class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.CharField(max_length=250, null=False)
    type = models.CharField(max_length=250, null=False)
    description = models.CharField(max_length=250, null=False)
    date = models.DateField(default=timezone.now().date())
    time = models.TimeField(default=timezone.now().time())
    flag = models.BooleanField(default=False)
