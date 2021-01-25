from django.shortcuts import render
from device.models import Device


def index(request):
    all_devices = Device.objects.all()
    args = {'devices': all_devices}
    return render(request, 'index.html', args)