from django.db import models
from django.contrib.auth.models import User


# device object
class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.CharField(max_length=250, null=False)
    deviceType = models.CharField(max_length=250, null=False)
    host = models.CharField(max_length=250, null=False)
    vendor = models.CharField(max_length=250, null=False)
    location = models.CharField(max_length=250, default='Not Specified')
    contact = models.CharField(max_length=250, default='Not Specified')
    status = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return self.device

