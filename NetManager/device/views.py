from django.contrib import messages
from .models import Device
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from netmiko import ConnectHandler


# device HTML view
def get_device(PageRequest, device_ID):
    try:
        # get selected device from db
        selected_device = Device.objects.get(pk=device_ID)
        # get devices IP address
        host = selected_device.host
        # pass device information to html
        args = {'device': selected_device, 'interfaces': get_interfaces(host), 'version': get_version(host), 'acl': get_acl(host)}
    except Device.DoesNotExist:
        raise Http404()
    return render(PageRequest, 'device.html', args)


# connect to host device
def connect(host):
    device = {
        'device_type': 'cisco_ios',
        'ip': host,
        'username': 'admin',
        'password': 'cisco',
        'secret': 'cisco',
        'port': 22
    }
    return device


# get device interfaces
def get_interfaces(host):
    # establish connection to device
    device = connect(host)

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
def get_version(host):
    # establish connection to device
    device = connect(host)

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
def get_acl(host):
    # establish connection to device
    device = connect(host)

    # open connection & run command
    try:
        c = ConnectHandler(**device)
        # store output in python dictionary using TextFSM
        output = c.send_command('show ip access-lists', use_textfsm=True)
        c.disconnect()
    except Exception as e:
        output = e
    return output


# function to save current configuration
def save_config(PageRequest, device_ID):
    # get devices IP address
    host = Device.objects.get(pk=device_ID).host

    # establish connection to device
    device = connect(host)

    try:
        c = ConnectHandler(**device)
        c.save_config()
        c.disconnect()
        return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))
    except Exception as e:
        return e


# configure an interfaces IP Address
def config_interface(PageRequest, device_ID):
    # get device from db
    host = Device.objects.get(pk=device_ID).host

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
        return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))
    except Exception as e:
        return e


# reset an interface
def reset_interface(PageRequest, device_ID):
    # get devices IP address
    host = Device.objects.get(pk=device_ID).host

    # get form data from POST request
    interface = PageRequest.POST.get('resetInterface')

    device = connect(host)

    try:
        c = ConnectHandler(**device)
        c.enable()
        commands = ['interface ' + interface, 'no ip address', 'shutdown']
        c.send_config_set(commands)
        c.disconnect()
        return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))
    except Exception as e:
        return e
