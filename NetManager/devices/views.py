"""

DEVICE/VIEWS.PY
* DEVICE PAGE
    * DEVICE CONNECTIONS
    * DEVICE CONFIGURATION
* INTERFACE PAGE
    * INTERFACE CONFIGURATION

"""
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from devices import device_controller as controller
from devices.forms import *
from devices.models import *


# redirect back to page
def refer(PageRequest, message):
    messages.success(PageRequest, message)
    return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))


''' *** devices list view *** '''


@login_required
def device_manager_view(PageRequest):
    form = DeviceForm(PageRequest.POST or None)
    user_devices = Device.objects.filter(user__username=PageRequest.user)
    date = datetime.datetime.now() - datetime.timedelta(days=1)
    config_logs = Alert.objects.filter(user__username=PageRequest.user, date__gt=date)
    args = {'devices': user_devices, 'status': controller.connect_test(user_devices), 'config_logs': config_logs,
            'form': form}
    return render(PageRequest, 'device_manager.html', args)


# add devices to db - ERROR HANDLING
@login_required
def add_device(PageRequest):
    form = DeviceForm(PageRequest.POST or None)
    user = User.objects.get(username=PageRequest.user)
    if form.is_valid():
        # d = Device
        d = form.save(commit=False)
        d.user = user
        d.save()
        Security.create_security(d)
    return refer(PageRequest, True)


''' *** devices configuration view *** '''


@login_required
def device_details_view(PageRequest, device_id):
    # get selected devices from db
    try:
        d = Device.get_device(device_id)
        int_form = InterfaceForm(PageRequest.POST or None)
        acl_form = AclForm(PageRequest.POST or None)
        args = {'device': d, 'int_form': int_form, 'acl_form': acl_form, 'interfaces': controller.get_interfaces(d),
                'version': controller.get_version(d), 'acl': controller.get_acl(d)}
    except Device.DoesNotExist:
        messages.error(PageRequest, 'Invalid URL: Device does not exist')
        return redirect('devices-list')
    return render(PageRequest, 'device_details.html', args)


# always returns /devices
@login_required
def save_config(PageRequest, device_id):
    d = Device.get_device(device_id)
    save = controller.save_config(d)
    return refer(PageRequest, save)


# always returns /devices
@login_required
def config_interface(PageRequest, device_id):
    global c
    d = Device.get_device(device_id)
    form = InterfaceForm(PageRequest.POST or None)
    if form.is_valid():
        c = controller.config_interface(d, form)
    return refer(PageRequest, str(c))


# always returns /devices
@login_required
def reset_interface(PageRequest, device_id):
    global c
    d = Device.get_device(device_id)
    i = PageRequest.POST.get('reset')
    c = controller.reset_interface(d, i)
    return refer(PageRequest, str(c))


# always returns /devices
@login_required
def disable_interfaces(PageRequest, device_id):
    global c
    d = Device.get_device(device_id)
    c = controller.disable_interfaces(d)
    return refer(PageRequest, str(c))


# always returns /devices
@login_required
def create_access_list(PageRequest, device_id):
    global c
    d = Device.get_device(device_id)
    form = AclForm(PageRequest.POST or None)
    if form.is_valid():
        c = controller.configure_acl(d, form)
    return refer(PageRequest, str(c))


# always returns /devices
@login_required
def delete_access_list(PageRequest, device_id):
    global c
    d = Device.get_device(device_id)
    acl = PageRequest.POST.get('acl')
    c = controller.delete_acl(d, acl)
    return refer(PageRequest, str(c))


''' *** interface details view *** '''


# interface view
@login_required
def interface_details_view(PageRequest, device_id, interface):
    try:
        i = interface
        print(i)
        d = Device.get_device(device_id)
        args = {'device': d, 'interface': i, 'details': controller.get_interface_details(d, i),
                'int_acl': controller.get_interface_ip(d, i), 'acl': controller.get_acl(d)}
    except Device.DoesNotExist:
        messages.error(PageRequest, 'Invalid URL: Device does not exist')
        return redirect('devices:device-config', device_id)
    return render(PageRequest, 'device_interface.html', args)


# always returns /devices
@login_required
def apply_access_list(PageRequest, device_id, interface):
    global c
    i = interface
    d = Device.get_device(device_id)
    acl = PageRequest.POST.get('acl')
    direction = PageRequest.POST.get('dir')
    c = controller.apply_acl(d, i, acl, direction)
    return refer(PageRequest, str(c))


# always returns /devices
@login_required
def remove_access_list(PageRequest, device_id, interface):
    global c
    i = interface
    d = Device.get_device(device_id)
    # annoying form implementation
    acl = PageRequest.POST.get('acl')
    direction = PageRequest.POST.get('dir')
    c = controller.remove_acl(d, i, acl, direction)
    return refer(PageRequest, str(c))


''' *** device manager view *** '''


# devices details view
@login_required
def device_settings_view(PageRequest, device_id):
    d = Device.get_device(device_id)
    # get security object based on devices id
    device_form = DeviceForm(PageRequest.POST or None, instance=d)
    security_form = SecurityForm(PageRequest.POST or None, instance=Security.get_device_security(device_id))
    args = {'device': d, 'security_form': security_form, 'device_form': device_form}
    return render(PageRequest, 'device_settings.html', args)


# delete devices from db - ERROR HANDLING
@login_required
def delete_device(PageRequest, device_id):
    d = Device.get_device(device_id)
    d.delete()
    messages.success(PageRequest, 'Device Deleted')
    return redirect('devices:device-manager')


# edit existing devices in db - ERROR HANDLING
@login_required
def edit_device(PageRequest, device_id):
    d = Device.get_device(device_id)
    form = DeviceForm(PageRequest.POST or None, instance=d)
    if form.is_valid():
        d.save()
    return refer(PageRequest, True)


# update devices log in information - ERROR HANDLING
@login_required
def device_security(PageRequest, device_id):
    s = Security.get_device_security(device_id)
    form = SecurityForm(PageRequest.POST or None, instance=s)
    if form.is_valid():
        s.save()
    return refer(PageRequest, True)
