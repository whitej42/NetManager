"""

DEVICE/VIEWS.PY
* DEVICE PAGE
    * DEVICE CONNECTIONS
    * DEVICE CONFIGURATION
* INTERFACE PAGE
    * INTERFACE CONFIGURATION

"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from device import device_controller as controller
from device.forms import *
from device.models import *


# redirect back to page
def refer(PageRequest, message):
    messages.success(PageRequest, message)
    return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))


''' *** device configuration view *** '''


# device view
# returns /device or /home
@login_required
def device_view(PageRequest, device_ID):
    # get selected device from db
    try:
        d = Device.get_device(device_ID)
        int_form = InterfaceForm(PageRequest.POST or None)
        acl_form = AclForm(PageRequest.POST or None)
        args = {'device': d, 'int_form': int_form, 'acl_form': acl_form, 'interfaces': controller.get_interfaces(d),
                'version': controller.get_version(d), 'acl': controller.get_acl(d)}
    except Device.DoesNotExist:
        messages.error(PageRequest, 'Invalid URL: Device does not exist')
        return redirect('home')
    return render(PageRequest, 'device.html', args)


# always returns /device - OPTIMIZED
def save_config(PageRequest, device_ID):
    d = Device.get_device(device_ID)
    save = controller.save_config(d)
    return refer(PageRequest, save)


# always returns /device - OPTIMIZED
def config_interface(PageRequest, device_ID):
    global c
    d = Device.get_device(device_ID)
    form = InterfaceForm(PageRequest.POST or None)
    if form.is_valid():
        c = controller.config_interface(d, form)
    return refer(PageRequest, str(c))


# always returns /device - OPTIMIZED
def reset_interface(PageRequest, device_ID):
    global c
    d = Device.get_device(device_ID)
    i = PageRequest.POST.get('interface')
    c = controller.reset_interface(d, i)
    return refer(PageRequest, str(c))


# always returns /device - OPTIMIZED
def disable_interfaces(PageRequest, device_ID):
    global c
    d = Device.get_device(device_ID)
    c = controller.disable_interfaces(d)
    return refer(PageRequest, str(c))


# always returns /device
def create_access_list(PageRequest, device_ID):
    global c
    d = Device.get_device(device_ID)
    form = AclForm(PageRequest.POST or None)
    if form.is_valid():
        c = controller.configure_acl(d, form)
    return refer(PageRequest, str(c))


# always returns /device
def delete_access_list(PageRequest, device_ID):
    global c
    d = Device.get_device(device_ID)
    acl = PageRequest.POST.get('acl')
    c = controller.delete_acl(d, acl)
    return refer(PageRequest, str(c))


''' *** interface details view *** '''


# interface view
@login_required
def interface_view(PageRequest, device_ID):
    try:
        d = Device.get_device(device_ID)
        i = PageRequest.POST.get('interface')
        form = ApplyAclForm(PageRequest.POST or None)
        args = {'device': d, 'form': form, 'interface': controller.get_interface_details(d, i),
                'int_acl': controller.get_interface_ip(d, i), 'acl': controller.get_acl(d)}
    except Device.DoesNotExist:
        messages.error(PageRequest, 'Invalid URL: Device does not exist')
        return redirect('home')
    return render(PageRequest, 'interface.html', args)


def apply_access_list(PageRequest, device_ID):
    global c
    d = Device.get_device(device_ID)
    # annoying form implementation
    i = PageRequest.POST.get('int')
    acl = PageRequest.POST.get('acl')
    direction = PageRequest.POST.get('dir')
    c = controller.apply_acl(d, i, acl, direction)
    messages.success(PageRequest, str(c))
    return redirect('device', device_ID)


def remove_access_list(PageRequest, device_ID):
    global c
    d = Device.get_device(device_ID)
    # annoying form implementation
    i = PageRequest.POST.get('int')
    acl = PageRequest.POST.get('acl')
    direction = PageRequest.POST.get('dir')
    c = controller.remove_acl(d, i, acl, direction)
    messages.success(PageRequest, str(c))
    return redirect('device', device_ID)
