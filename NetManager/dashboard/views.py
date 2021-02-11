from django.shortcuts import render
from device.models import Device


def index(PageRequest):
    all_devices = Device.objects.all()
    args = {'devices': all_devices}
    return render(PageRequest, 'index.html', args)