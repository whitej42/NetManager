import json
from django.shortcuts import render
from django.http import Http404
from .models import Device


def index(request):
    all_devices = Device.objects.all()
    args = {'devices': all_devices}
    return render(request, 'index.html', args)


def device(request, device_ID):
    try:
        with open('static/json/interfaces.json') as f:
            interfaces = json.load(f)
        args = {'device': Device.objects.get(pk=device_ID), 'interfaces': interfaces}
    except Device.DoesNotExist:
        raise Http404("Device does not exist")
    return render(request, 'device.html', args)
