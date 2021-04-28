from django.contrib import admin

from devices.models import Device, Security, Alert, Backup

admin.site.register(Device)
admin.site.register(Alert)
admin.site.register(Security)
admin.site.register(Backup)

