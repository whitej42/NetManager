"""

File: devices/forms.py

Purpose:
    This code defines the models for the devices application.
    These are stored in the sqlite3 database

"""
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# network device
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


# devices login credentials
class Security(models.Model):
    id = models.AutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    username = models.CharField(max_length=250, blank=True, null=True)
    password = models.CharField(max_length=250, blank=True, null=True)
    secret = models.CharField(max_length=250, blank=True, null=True)

    # create empty security object
    def create_blank_security(self):
        s = Security.objects.create(device_id=self.id)
        s.save()

    # get device object
    def get_device_security(self):
        security = Security.objects.get(device=self)
        return security

    # get devices username
    def get_username(self):
        username = Security.objects.filter(device=self.id).get().username
        return username

    # get devices password
    def get_password(self):
        password = Security.objects.filter(device=self.id).get().password
        return password

    # get devices secret
    def get_secret(self):
        secret = Security.objects.filter(device=self.id).get().secret
        return secret


# audit log alerts
class Alert(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.CharField(max_length=250, null=False)
    type = models.CharField(max_length=250, null=False)
    description = models.CharField(max_length=250, null=False)
    date = models.DateField(default=timezone.now().date())
    time = models.TimeField(default=timezone.now().time())

    def create_alert(self, device, type, description):
        a = Alert.objects.create(user=self, device=device, type=type, description=description)
        a.save()