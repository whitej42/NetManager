from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from manager.models import Device
from device.models import Log
from netmiko import ConnectHandler


# dashboard view
@login_required
def dashboard(PageRequest, username):
    user_devices = Device.objects.filter(user__username=username)
    config_logs = Log.objects.all()
    args = {'all_devices': user_devices, 'status': check_devices(), 'all_logs': config_logs}
    return render(PageRequest, 'dashboard.html', args)


# reports view
@login_required
def reports(PageRequest):
    all_devices = Device.objects.all()
    config_logs = Log.objects.all()
    args = {'all_devices': all_devices, 'all_logs': config_logs}
    return render(PageRequest, 'reports.html', args)


# test connection to all devices
def check_devices():
    user_devices = Device.objects.all()
    for i in user_devices:
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