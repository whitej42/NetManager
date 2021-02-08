import json
from dotenv import load_dotenv
from .models import Device
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from netmiko import ConnectHandler


# device view
def get_device(request, device_ID):
    try:
        # get selected device from db
        selected_device = Device.objects.get(pk=device_ID)
        # get devices ip address
        ip = selected_device.host
        # pass device information to html
        args = {'device': selected_device, 'interfaces': get_interfaces(ip), 'version': get_version(ip)}
    except Device.DoesNotExist:
        raise Http404()
    return render(request, 'device.html', args)


# connect to device
def connect(ip):
    import os
    from dotenv import load_dotenv

    load_dotenv()

    # user = os.environ.get('username')
    password = os.environ.get('password')
    secret = os.environ.get('secret')

    device = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': 'admin',
        'password': password,
        'secret': secret,
        'port': 22
    }

    return device


# function to get device interfaces - MOVE TO API LATER!
def get_interfaces(ip):

    device = connect(ip)

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


# function to get device version - MOVE TO API LATER
def get_version(ip):
    from netmiko import ConnectHandler

    device = connect(ip)

    # open connection & run command
    try:
        c = ConnectHandler(**device)
        # store output in python dictionary using TextFSM
        version = c.send_command('show version', use_textfsm=True)
        output = version
        c.disconnect()
    except Exception as e:
        output = e

    return output