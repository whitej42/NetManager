from django.contrib import admin

from devices.models import Device, Security, Alert

admin.site.register(Device)
admin.site.register(Alert)
admin.site.register(Security)
