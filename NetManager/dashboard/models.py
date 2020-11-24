from django.db import models


# device object
class Device(models.Model):
    device = models.CharField(max_length=250)
    deviceType = models.CharField(max_length=250)
    vendor = models.CharField(max_length=250)
    interfaces = models.IntegerField()

    def __str__(self):
        return 'Device: {}'.format(self.device)


# interface object
class Interface(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    interface = models.CharField(max_length=250)
    ipAddress = models.CharField(max_length=250)
    subnet = models.CharField(max_length=250)
    status = models.CharField(max_length=250)

    def __str__(self):
        return 'Interface: {}'.format(self.interface)
