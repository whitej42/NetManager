from django.shortcuts import render
from device.models import Device
from netmiko import ConnectHandler


def index(PageRequest):
    all_devices = Device.objects.all()
    args = {'devices': all_devices, 'status': check_devices()}
    return render(PageRequest, 'index.html', args)


def check_devices():
    all_devices = Device.objects.all()
    for i in all_devices:
        device = {'device_type': 'cisco_ios', 'ip': i.host, 'username': i.username, 'password': i.password,
                  'port': 22}
        try:
            c = ConnectHandler(**device)
            i.status = True
            i.save()
            c.disconnect()
        except:
            i.status = False
            i.save()