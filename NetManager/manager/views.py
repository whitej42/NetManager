from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from .models import Device
from device.models import Log
from django.contrib import messages
from .forms import DeviceForm


# device manager view
@login_required
def device_manager(PageRequest):
    form = DeviceForm(PageRequest.POST or None)
    all_devices = Device.objects.all()
    args = {'all_devices': all_devices, 'form': form}
    return render(PageRequest, 'manager.html', args)


# add device to db
def add_device(PageRequest):

    if PageRequest.method == 'POST':
        form = DeviceForm(PageRequest.POST or None)
        if form.is_valid():
            n = form.cleaned_data['device']
            PageRequest.user.Device_set.create(name=n)

    return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))


# edit existing device in db
def edit_device(PageRequest):
    device = PageRequest.POST.get('device')
    deviceType = PageRequest.POST.get('type')
    vendor = PageRequest.POST.get('vendor')
    host = PageRequest.POST.get('host')
    location = PageRequest.POST.get('loc')
    contact = PageRequest.POST.get('cont')

    try:
        d = Device.objects.get(pk=device)
        d.deviceType = deviceType
        d.vendor = vendor
        d.host = host
        d.location = location
        d.contact = contact
        d.save()
    except Device.DoesNotExist:
        raise Http404('Device Does Not Exist')

    log = Log(device=device, user='jwhite', type='Device', description='Device: ' + device + ' - Changes Applied ')
    log.save()
    messages.success(PageRequest, log.description)
    return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))


# delete device from db
def delete_device(PageRequest):
    device = PageRequest.POST.get('device')
    d = Device.objects.get(device=device)
    d.delete()
    log = Log(device=device, user='jwhite', type='Device',
              description='Device: ' + device + ' - Removed From Database')
    log.save()
    messages.success(PageRequest, log.description)
    return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))
