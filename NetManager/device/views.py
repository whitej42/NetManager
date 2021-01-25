from .models import Device
from django.http import Http404
from django.shortcuts import render


# device view
def get_device(request, device_ID):
    try:
        # get selected device from db
        selected_device = Device.objects.get(pk=device_ID)
        # get devices ip address
        ip = selected_device.host
        # pass device information to html
        args = {'device': selected_device, 'interfaces': get_interfaces(ip)}
    except Device.DoesNotExist:
        raise Http404()
    return render(request, 'device.html', args)


# function to get device interfaces - MOVE TO API LATER!
def get_interfaces(ip):
    import os
    from netmiko import ConnectHandler
    from dotenv import load_dotenv

    load_dotenv()

    # user = os.environ.get('username')
    password = os.environ.get('password')
    secret = os.environ.get('secret')

    router = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': 'admin',
        'password': password,
        'secret': secret,
        'port': 22
    }

    # open connection & run command
    try:
        c = ConnectHandler(**router)
        # store output in python dictionary using TextFSM
        interfaces = c.send_command('show ip int brief', use_textfsm=True)
        c.disconnect()
        return interfaces
    except Exception as e:
        print(e)
