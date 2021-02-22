from django.db import models


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
