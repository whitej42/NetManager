"""

MAIN/VIEWS.PY
* MAIN PAGE
    * CHECK CONNECTIONS
    * ADD NEW DEVICES
* PROFILE PAGE
    * UPDATE USER PROFILE
    * CHANGE PASSWORD
    * DELETE ACCOUNT

"""


import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from device.models import *
from home.forms import *
from device import device_controller as controller


# redirect back to page after form submission
def refer(PageRequest, message):
    messages.success(PageRequest, message)
    return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))


# home view
@login_required
def home(PageRequest):
    form = DeviceForm(PageRequest.POST or None)
    user_devices = Device.objects.filter(user__username=PageRequest.user)
    date = datetime.datetime.now() - datetime.timedelta(days=1)
    config_logs = Alert.objects.filter(user__username=PageRequest.user, date__gt=date)
    args = {'all_devices': user_devices, 'status': controller.connect_test(user_devices), 'config_logs': config_logs, 'form': form}
    return render(PageRequest, 'home.html', args)


# device details view
@login_required
def details(PageRequest, device_ID):
    device = Device.objects.filter(id=device_ID)
    device_form = DeviceForm(PageRequest.POST or None, instance=device.get())
    security_form = SecurityForm(PageRequest.POST or None, instance=device.get())
    args = {'device': device, 'security_form': security_form, 'device_form': device_form}
    return render(PageRequest, 'details.html', args)


# reports view
@login_required
def reports(PageRequest):
    user_devices = Device.objects.filter(user__username=PageRequest.user)
    config_logs = Alert.objects.filter(user__username=PageRequest.user)
    args = {'all_devices': user_devices, 'config_logs': config_logs}
    return render(PageRequest, 'reports.html', args)


# add device to db
def add_device(PageRequest):
    form = DeviceForm(PageRequest.POST or None)

    try:
        if PageRequest.user.is_authenticated:
            if form.is_valid():
                device = form.save(commit=False)
                device.user_id = User.objects.get(username=PageRequest.user).pk
                device.save()
                alert = Alert(user=PageRequest.user, device=device, type='Device',
                              description='Device: ' + device.name + ' - Added to database')
                alert.save()
                return refer(PageRequest, alert.description)
    except Exception as e:
        messages.error(PageRequest, str(e))
        return redirect(home)


# delete device from db
def delete_device(PageRequest):
    try:
        device_id = PageRequest.POST.get('id')
        d = Device.objects.get(pk=device_id)
        d.delete()
        alert = Alert(user=PageRequest.user, device=d.name, type='Device',
                      description='Device: ' + d.name + ' - Removed from database')
        alert.save()
        return redirect(home)
    except Exception as e:
        messages.error(PageRequest, str(e))
        return redirect(home)


# edit existing device in db
def edit_device(PageRequest):
    device = Device.objects.get(pk=PageRequest.POST.get('id'))
    form = DeviceForm(PageRequest.POST or None, instance=device)

    try:
        if PageRequest.user.is_authenticated:
            if form.is_valid():
                device.save()
        alert = Alert(user=PageRequest.user, device=device.name, type='Device',
                      description='Changes made to device: ' + device.name)
        alert.save()
        return refer(PageRequest, alert.description)
    except Exception as e:
        messages.error(PageRequest, str(e))
        return redirect(home)


# update device log in information
def update_security(PageRequest):
    device_id = PageRequest.POST.get('id')
    device = Device.objects.get(pk=device_id)
    form = SecurityForm(PageRequest.POST or None, instance=device)

    try:
        if PageRequest.user.is_authenticated:
            if form.is_valid():
                device.save()
        alert = Alert(user=PageRequest.user, device=device.name, type='Security',
                      description='Device: ' + device.name + ' - Security settings changed')
        alert.save()
        return refer(PageRequest, alert.description)
    except Exception as e:
        messages.error(PageRequest, str(e))
        return redirect(home)