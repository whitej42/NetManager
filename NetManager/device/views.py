from django.contrib.auth.decorators import login_required
from .models import Device
from .models import Log
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from netmiko import ConnectHandler


# device HTML view
@login_required
def get_device(PageRequest, device_ID):
    try:
        # get selected device from db
        selected_device = Device.objects.get(pk=device_ID)
        # get devices IP address
        host = selected_device.host
        # pass device information to html
        args = {'device': selected_device, 'interfaces': get_interfaces(host), 'version': get_version(host),
                'acl': get_acl(host)}
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
        log = Log(device=device_ID, user='jwhite', type='Configuration',
                  description='Device configuration saved')
        log.save()
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
        log = Log(device=device_ID, user='jwhite', type='Configuration',
                  description='IP Address ' + address + ' configured on interface ' + interface)
        log.save()
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
        log = Log(device=device_ID, user='jwhite', type='Configuration',
                  description='Interface ' + interface + ' reset')
        log.save()
        return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))
    except Exception as e:
        return e


# create access list
def create_acl(PageRequest, device_ID):
    # get devices IP address
    host = Device.objects.get(pk=device_ID).host

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
        log = Log(device=device_ID, user='jwhite', type='Security',
                  description='Access List ' + acl_name + ' configured')
        log.save()
        return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))
    except Exception as e:
        return e


# delete access list
def delete_acl(PageRequest, device_ID):
    host = Device.objects.get(pk=device_ID).host

    acl = PageRequest.POST.get('del_acl')

    device = connect(host)

    try:
        c = ConnectHandler(**device)
        c.enable()
        commands = ['no ip access-list ' + acl]
        c.send_config_set(commands)
        c.disconnect()
        log = Log(device=device_ID, user='jwhite', type='Security',
                  description='Access List ' + acl + ' removed')
        log.save()
        return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))
    except Exception as e:
        return e


# apply access list
def apply_acl(PageRequest, device_ID):
    host = Device.objects.get(pk=device_ID).host

    interface = PageRequest.POST.get('ACLInterface')
    acl = PageRequest.POST.get('app_acl')
    direction = PageRequest.POST.get('dir_acl')

    device = connect(host)

    try:
        c = ConnectHandler(**device)
        c.enable()
        commands = ['interface ' + interface, 'ip access-group ' + acl + ' ' + direction]
        c.send_config_set(commands)
        c.disconnect()
        log = Log(device=device_ID, user='jwhite', type='Security',
                  description='Access List ' + acl + ' applied to ' + interface)
        log.save()
        return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))
    except Exception as e:
        return e


# configure banners - NOT WORKING!
def config_banner(PageRequest, device_ID):
    host = Device.objects.get(pk=device_ID).host

    banner_type = PageRequest.POST.get('banner_type')
    banner_txt = PageRequest.POST.get('banner_txt')
    n = len(banner_txt) + 2
    border = '*' * n

    device = connect(host)

    try:
        c = ConnectHandler(**device)
        c.enable()
        c.send_command('banner ' + banner_type + ' ^')
        c.send_command(border)
        c.send_command(' ' + banner_txt)
        c.send_command(border + '^')
        c.disconnect()
        return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))
    except Exception as e:
        return e


# disable unused interfaces
def disable_interfaces(PageRequest, device_ID):
    host = Device.objects.get(pk=device_ID).host

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
        log = Log(device=device_ID, user='jwhite', type='Security',
                  description='All unused interfaces shutdown')
        log.save()
        return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))
    except Exception as e:
        return e
