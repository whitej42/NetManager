"""

DEVICE/MODELS.PY

* DEVICE
    * USER DEVICES

* SECURITY
    * DEVICE SECURITY SETTINGS

* ALERT
    * CONFIGURATION ALERT

"""

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Device(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=False)
    type = models.CharField(max_length=250, null=False)
    host = models.CharField(max_length=250, null=False)
    vendor = models.CharField(max_length=250, null=False)
    location = models.CharField(max_length=250, default='Not Specified')
    contact = models.CharField(max_length=250, default='Not Specified')
    status = models.BooleanField(default=False, editable=False)

    def get_device(self):
        device = Device.objects.get(id=self)
        return device


class Security(models.Model):
    id = models.AutoField(primary_key=True)
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
    username = models.CharField(max_length=250, blank=True, null=True)
    password = models.CharField(max_length=250, blank=True, null=True)
    secret = models.CharField(max_length=250, blank=True, null=True)

    def create_security(self):
        s = Security.objects.create(device_id=self)
        s.save()

    def get_device_security(self):
        security = Security.objects.get(device_id=self)
        return security

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
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.CharField(max_length=250, null=False)
    type = models.CharField(max_length=250, null=False)
    description = models.CharField(max_length=250, null=False)
    date = models.DateField(default=timezone.now().date())
    time = models.TimeField(default=timezone.now().time())
    flag = models.BooleanField(default=False)

    #def create_alert(self):
        #do something
