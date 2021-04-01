"""

DEVICE/VIEWS.PY
* DEVICE PAGE
    * DEVICE CONNECTIONS
    * DEVICE CONFIGURATION
* INTERFACE PAGE
    * INTERFACE CONFIGURATION

"""

from .models import Log
from device.models import Device
from netmiko import ConnectHandler
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, HttpResponse


# connect to host device
def connect(d):
    device = {
        'device_type': 'cisco_ios',
        'ip': d.host,
        'username': d.username,
        'password': d.password,
        'secret': d.secret,
        'port': 22
    }
    return device


# retrieve device information
def retrieve(d, command):
    try:
        c = ConnectHandler(**connect(d))
        output = c.send_command(command, use_textfsm=True)
        c.disconnect()
    except Exception as e:
        output = e
    return output


# send commands to device
def configure(d, command):
    try:
        c = ConnectHandler(**connect(d))
        c.enable()
        c.send_config_set(command)
        c.disconnect()
        # 1 = success
        return 1
    except Exception as e:
        return e


# redirect back to page after form submission
def refer(PageRequest, message):
    messages.success(PageRequest, message)
    return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))


''' *** Functions for the device configuration page *** '''


# device HTML view
@login_required
def device(PageRequest, device_ID):
    try:
        # get selected device from db
        selected_device = Device.objects.get(pk=device_ID)
        # pass device information to template
        args = {'device': selected_device, 'interfaces': get_interfaces(selected_device),
                'version': get_version(selected_device),
                'acl': get_acl(selected_device)}
    except Device.DoesNotExist:
        raise Http404('Device Does Not Exist')
    return render(PageRequest, 'device.html', args)


# get device interfaces
def get_interfaces(selected_device):
    output = retrieve(selected_device, 'show ip interface brief')
    return output


# get device version
def get_version(selected_device):
    output = retrieve(selected_device, 'show version')
    return output


# get devices access-lists
def get_acl(selected_device):
    # open connection & run command
    output = retrieve(selected_device, 'show ip access-lists')
    return output


# save current configuration
def save_config(PageRequest, device_ID):
    # get devices IP address
    host = Device.objects.get(pk=device_ID)

    try:
        c = ConnectHandler(**connect(host))
        # save config with NetMiko save_config() function
        c.save_config()
        c.disconnect()
        l = Log(user=PageRequest.user, device=host.name, type='Configuration',
                description='Device configuration saved')
        l.save()
        messages.success(PageRequest, l.description)
        return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))
    except Exception as e:
        messages.success(PageRequest, e)
        return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))


def config_interface(PageRequest, device_ID, action):
    global cmd, l
    host = Device.objects.get(pk=device_ID)

    if action == 'CONFIG':
        selected_interface = PageRequest.POST.get('configInterface')
        address = PageRequest.POST.get('ip')
        mask = PageRequest.POST.get('mask')
        enable = PageRequest.POST.get('enable')

        if enable == 'on':
            cmd = ['interface ' + selected_interface, 'ip address ' + address + ' ' + mask, 'no shutdown']
        else:
            cmd = ['interface ' + selected_interface, 'ip address ' + address + ' ' + mask, 'shutdown']

        l = Log(user=PageRequest.user, device=host.name, type='Configuration',
                description='IP Address ' + address + ' configured on interface ' + selected_interface)

    if action == 'RESET':
        selected_interface = PageRequest.POST.get('resetInterface')
        cmd = ['interface ' + selected_interface, 'no ip address', 'shutdown']
        l = Log(user=PageRequest.user, device=host.name, type='Configuration',
                description='Interface ' + selected_interface + ' reset')

    c = configure(host, cmd)
    if c == 1:
        l.save()
        return refer(PageRequest, l.description)
    else:
        return refer(PageRequest, 'Command Failed: ' + str(c))


# disable unused interfaces
def disable_interfaces(PageRequest, device_ID):
    host = Device.objects.get(pk=device_ID)

    # cannot use configure() or retrieve() functions - slow execution time

    try:
        c = ConnectHandler(**connect(device))
        c.enable()
        interfaces = c.send_command('show ip int brief', use_textfsm=True)
        for i in interfaces:
            if i['ipaddr'] == 'unassigned' and i['status'] != 'administratively down':
                cmd = ['interface ' + i['intf'], 'shutdown']
                c.send_config_set(cmd)
        l = Log(user=PageRequest.user, device=host.name, type='Security',
                description='All unused interfaces shutdown')
        l.save()
        return refer(PageRequest, l.description)
    except Exception as e:
        return refer(PageRequest, 'Command Failed: ' + str(e))


# create & delete access lists
def access_list(PageRequest, device_ID, action):
    # action = 'CREATE', 'DELETE
    global cmd, l
    host = Device.objects.get(pk=device_ID)

    if action == 'CREATE':
        acl_type = PageRequest.POST.get('acl_type')
        acl_name = PageRequest.POST.get('acl_name')
        acl = PageRequest.POST.get('acl')
        cmd = ['ip access-list ' + acl_type + " " + acl_name, acl]
        l = Log(user=PageRequest.user, device=host.name, type='Security',
                description='Access List ' + acl_name + ' configured')

    if action == 'DELETE':
        acl = PageRequest.POST.get('del_acl')
        cmd = ['no ip access-list ' + acl]
        l = Log(user=PageRequest.user, device=host.name, type='Security',
                description='Access List ' + acl + ' removed')

    c = configure(host, cmd)
    if c == 1:
        l.save()
        return refer(PageRequest, l.description)
    else:
        return refer(PageRequest, 'Command Failed: ' + str(c))


''' *** Functions for the interface details page *** '''


# render interface details page
@login_required
def interface(PageRequest, device_ID):
    try:
        selected_device = Device.objects.get(pk=device_ID)
        selected_interface = PageRequest.POST.get('interface')
        args = {'device': selected_device, 'interface': interface_details(selected_device, selected_interface),
                'acl': get_acl(selected_device), 'int_acl': interface_ip_details(selected_device, selected_interface)}
    except Device.DoesNotExist:
        raise Http404()
    return render(PageRequest, 'interface.html', args)


# get interface details
def interface_details(selected_device, selected_interface):
    output = retrieve(selected_device, 'show interface ' + selected_interface)
    return output


def interface_ip_details(selected_device, selected_interface):
    output = retrieve(selected_device, 'show ip interface ' + selected_interface)
    return output


def interface_access_list(PageRequest, device_ID, action):
    # action = 'APPLY', 'REMOVE'
    global cmd, l
    host = Device.objects.get(pk=device_ID)

    selected_interface = PageRequest.POST.get('int')
    acl = PageRequest.POST.get('acl')
    direction = PageRequest.POST.get('dir')

    if action == 'APPLY':
        cmd = ['interface ' + selected_interface, 'ip access-group ' + acl + ' ' + direction]
        l = Log(user=PageRequest.user, device=host.name, type='Security',
                description='Access List ' + acl + ' applied to ' + selected_interface)
    if action == 'REMOVE':
        cmd = ['interface ' + selected_interface, 'no ip access-group ' + acl + ' ' + direction]
        l = Log(user=PageRequest.user, device=host.name, type='Security',
                description='Access List ' + acl + ' removed from ' + selected_interface)

    c = configure(host, cmd)
    if c == 1:
        messages.success(PageRequest, l.description)
        return redirect(device, device_ID=device_ID)
    else:
        messages.success(PageRequest, 'Command Failed: ' + str(c))
        return redirect(device, device_ID=device_ID)
