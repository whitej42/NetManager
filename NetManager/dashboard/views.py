from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from netmiko import ConnectHandler
from device.models import *
from dashboard.forms import *
import datetime


# dashboard view
@login_required
def dashboard(PageRequest):
    form = DeviceForm(PageRequest.POST or None)
    user_devices = Device.objects.filter(user__username=PageRequest.user)
    date = datetime.datetime.now() - datetime.timedelta(days=1)
    config_logs = Log.objects.filter(user__username=PageRequest.user, dateTime__gt=date)
    args = {'all_devices': user_devices, 'status': check_devices(), 'all_logs': config_logs, 'form': form}
    return render(PageRequest, 'dashboard.html', args)


@login_required
def details(PageRequest, device_ID):
    device = Device.objects.filter(id=device_ID)
    form = SecurityForm(PageRequest.POST or None)
    args = {'device': device, 'form': form}
    return render(PageRequest, 'details.html', args)


# reports view
@login_required
def reports(PageRequest):
    user_devices = Device.objects.filter(user__username=PageRequest.user)
    config_logs = Log.objects.filter(user__username=PageRequest.user)
    args = {'all_devices': user_devices, 'all_logs': config_logs}
    return render(PageRequest, 'reports.html', args)


# test connection to all devices
def check_devices():
    user_devices = Device.objects.all()
    for i in user_devices:
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


# add device to db
def add_device(PageRequest):
    form = DeviceForm(PageRequest.POST or None)
    if PageRequest.user.is_authenticated:
        if form.is_valid():
            device = form.save(commit=False)
            device.user_id = User.objects.get(username=PageRequest.user).pk
            device.save()
            log = Log(user=PageRequest.user, device=device, type='Device', description='Device: ' + device.deviceName + ' - Added to the Database')
            log.save()
            messages.success(PageRequest, log.description)
    return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))


# delete device from db
def delete_device(PageRequest):
    device_id = PageRequest.POST.get('id')
    d = Device.objects.get(pk=device_id)
    d.delete()
    log = Log(user=PageRequest.user, device=d.deviceName, type='Device', description='Device: ' + d.deviceName + ' - Removed From Database')
    log.save()
    messages.success(PageRequest, log.description)
    return redirect(dashboard)


# edit existing device in db
def edit_device(PageRequest):
    device_id = PageRequest.POST.get('id')
    device = PageRequest.POST.get('device')
    deviceType = PageRequest.POST.get('type')
    vendor = PageRequest.POST.get('vendor')
    host = PageRequest.POST.get('host')
    location = PageRequest.POST.get('loc')
    contact = PageRequest.POST.get('cont')

    try:
        d = Device.objects.get(pk=device_id)
        d.deviceName = device
        d.deviceType = deviceType
        d.vendor = vendor
        d.host = host
        d.location = location
        d.contact = contact
        d.save()
    except Device.DoesNotExist:
        raise Http404('Device Does Not Exist')

    log = Log(user=PageRequest.user, device=device, type='Device', description='Device: ' + device + ' - Changes Applied ')
    log.save()
    messages.success(PageRequest, log.description)
    return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))


# update device log in information
def update_security(PageRequest):
    device_id = PageRequest.POST.get('id')
    device = Device.objects.get(pk=device_id)
    form = SecurityForm(PageRequest.POST or None)

    if PageRequest.user.is_authenticated:
        if form.is_valid():
            device.username = form.cleaned_data['username']
            device.password = form.cleaned_data['password']
            device.secret = form.cleaned_data['secret']
            device.save()
    log = Log(user=PageRequest.user, device=device.deviceName, type='Security',
              description='Device: ' + device.deviceName + ' - Security Settings Changed')
    log.save()
    messages.success(PageRequest, log.description)
    return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))

