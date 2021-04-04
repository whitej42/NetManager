from django.contrib import admin

from device.models import Device, Security, Alert

admin.site.register(Device)
admin.site.register(Alert)
admin.site.register(Security)
