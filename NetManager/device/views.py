"""

DEVICE VIEWS.PY
* DEVICE PAGE
    * DEVICE CONNECTIONS
    * DEVICE CONFIGURATION
* INTERFACE PAGE
    * INTERFACE CONFIGURATION

"""

from django.contrib.auth.decorators import login_required
from device.models import Device
from .models import Log
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from netmiko import ConnectHandler
from django.contrib import messages


# connect to host device
def connect(selected_device):
    device = {
        'device_type': 'cisco_ios',
        'ip': selected_device.host,
        'username': selected_device.username,
        'password': selected_device.password,
        'secret': selected_device.secret,
        'port': 22
    }
    return device


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
    # establish connection to device
    device = connect(selected_device)

    # open connection & run command
    try:
        c = ConnectHandler(**device)
        # store output in python dictionary using TextFSM
        interfaces = c.send_command('show ip int brief', use_textfsm=True)
        output = interfaces
        c.disconnect()
    except Exception as e:
        output = e
    return output


# get device version
def get_version(selected_device):
    # establish connection to device
    device = connect(selected_device)

    # open connection & run command
    try:
        c = ConnectHandler(**device)
        # store output in python dictionary using TextFSM
        output = c.send_command('show version', use_textfsm=True)
        c.disconnect()
    except Exception as e:
        output = e
    return output


# get devices access-lists
def get_acl(selected_device):
    # establish connection to device
    device = connect(selected_device)

    # open connection & run command
    try:
        c = ConnectHandler(**device)
        # store output in python dictionary using TextFSM
        output = c.send_command('show ip access-lists', use_textfsm=True)
        c.disconnect()
    except Exception as e:
        output = e
    return output


# save current configuration
def save_config(PageRequest, device_ID):
    # get devices IP address
    host = Device.objects.get(pk=device_ID)

    # establish connection to device
    device = connect(host)

    try:
        c = ConnectHandler(**device)
        # save config using NetMiko save_config() function
        c.save_config()
        c.disconnect()
        log = Log(user=PageRequest.user, device=host.name, type='Configuration',
                  description='Device configuration saved')
        log.save()
        messages.success(PageRequest, log.description)
        return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))
    except Exception as e:
        return e


# configure an interfaces IP Address
def config_interface(PageRequest, device_ID):
    # get device from db
    host = Device.objects.get(pk=device_ID)

    # get form data from POST request
    interface = PageRequest.POST.get('configInterface')
    address = PageRequest.POST.get('ip')
    mask = PageRequest.POST.get('mask')
    enable = PageRequest.POST.get('enable')

    # establish connection to device
    device = connect(host)

    try:
        c = ConnectHandler(**device)
        c.enable()
        if enable == 'on':
            commands = ['interface ' + interface, 'ip address ' + address + ' ' + mask, 'no shutdown']
        else:
            commands = ['interface ' + interface, 'ip address ' + address + ' ' + mask, 'shutdown']
        c.send_config_set(commands)
        c.disconnect()
        log = Log(user=PageRequest.user, device=host.name, type='Configuration',
                  description='IP Address ' + address + ' configured on interface ' + interface)
        log.save()
        messages.success(PageRequest, log.description)
        return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))
    except Exception as e:
        return e


# reset an interface
def reset_interface(PageRequest, device_ID):
    # get devices IP address
    host = Device.objects.get(pk=device_ID)

    # get form data from POST request
    interface = PageRequest.POST.get('resetInterface')

    device = connect(host)

    try:
        c = ConnectHandler(**device)
        c.enable()
        commands = ['interface ' + interface, 'no ip address', 'shutdown']
        c.send_config_set(commands)
        c.disconnect()
        log = Log(user=PageRequest.user, device=host.name, type='Configuration',
                  description='Interface ' + interface + ' reset')
        log.save()
        messages.success(PageRequest, log.description)
        return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))
    except Exception as e:
        return e


# create access list
def create_acl(PageRequest, device_ID):
    # get devices IP address
    host = Device.objects.get(pk=device_ID)

    acl_type = PageRequest.POST.get('acl_type')
    acl_name = PageRequest.POST.get('acl_name')
    acl = PageRequest.POST.get('acl')

    device = connect(host)

    try:
        c = ConnectHandler(**device)
        c.enable()
        commands = ['ip access-list ' + acl_type + " " + acl_name, acl]
        c.send_config_set(commands)
        c.disconnect()
        log = Log(user=PageRequest.user, device=host.name, type='Security',
                  description='Access List ' + acl_name + ' configured')
        log.save()
        messages.success(PageRequest, log.description)
        return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))
    except Exception as e:
        return e


# delete access list
def delete_acl(PageRequest, device_ID):
    host = Device.objects.get(pk=device_ID)

    acl = PageRequest.POST.get('del_acl')

    device = connect(host)

    try:
        c = ConnectHandler(**device)
        c.enable()
        commands = ['no ip access-list ' + acl]
        c.send_config_set(commands)
        c.disconnect()
        log = Log(user=PageRequest.user, device=host.name, type='Security',
                  description='Access List ' + acl + ' removed')
        log.save()
        messages.success(PageRequest, log.description)
        return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))
    except Exception as e:
        return e


# disable unused interfaces
def disable_interfaces(PageRequest, device_ID):
    host = Device.objects.get(pk=device_ID)

    device = connect(host)

    try:
        c = ConnectHandler(**device)
        c.enable()
        interfaces = c.send_command('show ip int brief', use_textfsm=True)
        for interface in interfaces:
            if interface['ipaddr'] == 'unassigned' and interface['status'] != 'administratively down':
                commands = ['interface ' + interface['intf'], 'shutdown']
                c.send_config_set(commands)
        c.disconnect()
        log = Log(user=PageRequest.user, device=host.name, type='Security',
                  description='All unused interfaces shutdown')
        log.save()
        messages.success(PageRequest, log.description)
        return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))
    except Exception as e:
        return e


''' *** Functions for the interface details page *** '''


# interface details HTML view
@login_required
def interface(PageRequest, device_ID):
    # check item exists in db
    try:
        # get selected device from db
        selected_device = Device.objects.get(pk=device_ID)
        # get devices IP address
        # get selected interface
        selected_interface = PageRequest.POST.get('interface')
        # pass interface information to template
        args = {'device': selected_device, 'interface': interface_details(selected_device, selected_interface),
                'acl': get_acl(selected_device), 'int_acl': interface_acl(selected_device, selected_interface)}
    except Device.DoesNotExist:
        # if not - raise http404
        raise Http404()
    return render(PageRequest, 'interface.html', args)


# get interface details
def interface_details(host, interface):
    # establish connection to device
    device = connect(host)

    # open connection & run command
    try:
        c = ConnectHandler(**device)
        # store output in python dictionary using TextFSM
        output = c.send_command('show interface ' + interface, use_textfsm=True)
        c.disconnect()
    except Exception as e:
        output = e
    return output


# get acls applied to interface
def interface_acl(host, interface):
    # establish connection to device
    device = connect(host)

    # open connection & run command
    try:
        c = ConnectHandler(**device)
        # store output in python dictionary using TextFSM
        output = c.send_command('show ip interface ' + interface, use_textfsm=True)
        c.disconnect()
    except Exception as e:
        output = e
    return output


# apply access list
def apply_acl(PageRequest, device_ID):
    host = Device.objects.get(pk=device_ID)

    interface = PageRequest.POST.get('int')
    acl = PageRequest.POST.get('acl')
    direction = PageRequest.POST.get('dir')

    device = connect(host)

    try:
        c = ConnectHandler(**device)
        c.enable()
        commands = ['interface ' + interface, 'ip access-group ' + acl + ' ' + direction]
        c.send_config_set(commands)
        c.disconnect()
        log = Log(user=PageRequest.user, device=host.name, type='Security',
                  description='Access List ' + acl + ' applied to ' + interface)
        log.save()
        messages.success(PageRequest, log.description)
        return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))  # crashes on reload - no form submission!!
    except Exception as e:
        return e


def remove_acl(PageRequest, device_ID):
    host = Device.objects.get(pk=device_ID)

    interface = PageRequest.POST.get('int')
    acl = PageRequest.POST.get('acl')
    direction = PageRequest.POST.get('dir')

    device = connect(host)

    try:
        c = ConnectHandler(**device)
        c.enable()
        commands = ['interface ' + interface, 'no ip access-group ' + acl + ' ' + direction]
        c.send_config_set(commands)
        c.disconnect()
        log = Log(user=PageRequest.user, device=host.name, type='Security',
                  description='Access List ' + acl + ' removed from ' + interface)
        log.save()
        messages.success(PageRequest, log.description)
        return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))  # crashes on reload - no form submission!!
    except Exception as e:
        return e
