from django.db import models


# device object
class Device(models.Model):
    device = models.CharField(primary_key=True, max_length=250)
    deviceType = models.CharField(max_length=250)
    host = models.CharField(max_length=250)
    username = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    vendor = models.CharField(max_length=250)
    location = models.CharField(max_length=250, default='Not Specified')
    contact = models.CharField(max_length=250, default='Not Specified')
    status = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return self.device
