from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from device.models import Device
from device.models import Log


# device manager view
@login_required
def device_manager(PageRequest):
    all_devices = Device.objects.all()
    args = {'all_devices': all_devices, 'range': range(5)}
    return render(PageRequest, 'manager.html', args)


# add device to db
def add_device(PageRequest):
    device = PageRequest.POST.get('name')
    deviceType = PageRequest.POST.get('type')
    ssh = PageRequest.POST.get('ssh')
    vendor = PageRequest.POST.get('vendor')
    location = PageRequest.POST.get('location')
    contact = PageRequest.POST.get('contact')

    d = Device(device=device, deviceType=deviceType, host=ssh, vendor=vendor, location=location, contact=contact)
    d.save()
    log = Log(device=device, user='jwhite', type='Device',
              description='Device ' + device + ' added to database')
    log.save()
    return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))


# edit existing device in db
def edit_device(PageRequest):
    deviceType = PageRequest.POST.get('type')
    ssh = PageRequest.POST.get('ssh')
    vendor = PageRequest.POST.get('vendor')
    location = PageRequest.POST.get('location')
    contact = PageRequest.POST.get('contact')

    # log = Log(device=device, user='jwhite', type='Device', description='Device ' + device + ' added to database')
    # log.save()
    return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))


# delete device from db
def delete_device(PageRequest):
    device = PageRequest.POST.get('deleteDevice')
    d = Device.objects.get(pk=device)
    d.delete()
    log = Log(device=device, user='jwhite', type='Device',
              description='Device ' + device + ' removed from database')
    log.save()
    return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))
