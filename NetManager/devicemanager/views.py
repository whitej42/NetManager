from django.http import HttpResponseRedirect
from django.shortcuts import render
from device.models import Device


# device manager view
def device_manager(PageRequest):
    all_devices = Device.objects.all()
    args = {'all_devices': all_devices, 'range': range(5)}
    return render(PageRequest, 'manager.html', args)


def add_device(PageRequest):
    name = PageRequest.POST.get('name')
    DeviceType = PageRequest.POST.get('type')
    ssh = PageRequest.POST.get('ssh')
    vendor = PageRequest.POST.get('vendor')
    location = PageRequest.POST.get('location')
    contact = PageRequest.POST.get('contact')

    # TEMP FIX - CHANGE THIS!!!
    if name == "":
        return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))
    else:
        d = Device(device=name, deviceType=DeviceType, host=ssh, vendor=vendor, location=location, contact=contact)
        d.save()
        return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))


def delete_device(PageRequest):
    device = PageRequest.POST.get('deleteDevice')
    d = Device.objects.get(pk=device)
    d.delete()

    return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))