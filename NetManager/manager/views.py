from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from device.models import Log
from django.contrib import messages
from dashboard.forms import *
from django.contrib.auth.models import User


# device manager view
@login_required
def device_manager(PageRequest):
    device_form = DeviceForm(PageRequest.POST or None)
    security_form = SecurityForm(PageRequest.POST or None)
    user_devices = Device.objects.filter(user__username=PageRequest.user)
    args = {'all_devices': user_devices, 'dform': device_form, 'sform': security_form}
    return render(PageRequest, 'details.html', args)





# delete device from db
def delete_device(PageRequest):
    id = PageRequest.POST.get('id')
    d = Device.objects.get(pk=id)
    d.delete()
    log = Log(user=PageRequest.user, device=d.name, type='Device', description='Device: ' + d.name + ' - Removed From Database')
    log.save()
    messages.success(PageRequest, log.description)
    return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))


# update device log in information
def update_security(PageRequest):
    id = PageRequest.POST.get('id')
    device = Device.objects.get(pk=id)
    form = SecurityForm(PageRequest.POST or None)

    if PageRequest.user.is_authenticated:
        if form.is_valid():
            device.username = form.cleaned_data['username']
            device.password = form.cleaned_data['password']
            device.secret = form.cleaned_data['secret']
            device.save()
    log = Log(user=PageRequest.user, device=device.name, type='Device',
              description='Device: ' + device.name + ' - Added to the Database')
    log.save()
    messages.success(PageRequest, log.description)

    return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))