from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from device.models import Device
from device.models import Log
from netmiko import ConnectHandler


# dashboard view
@login_required
def index(PageRequest):
    all_devices = Device.objects.all()
    config_logs = Log.objects.all()
    args = {'all_devices': all_devices, 'status': check_devices(), 'all_logs': config_logs}
    return render(PageRequest, 'index.html', args)


# check connection to all devices
def check_devices():
    all_devices = Device.objects.all()
    for i in all_devices:
        device = {'device_type': 'cisco_ios', 'ip': i.host, 'username': 'admin', 'password': 'cisco',
                  'port': 22}
        try:
            c = ConnectHandler(**device)
            i.status = True
            i.save()
            c.disconnect()
        except:
            i.status = False
            i.save()