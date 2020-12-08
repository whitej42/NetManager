from django.shortcuts import render
from .models import *
from subprocess import run, PIPE
import sys


def index(request):
    devices = Device.objects.all()
    args = {'devices': devices}
    return render(request, 'index.html', args)



def connect(request):
    from netmiko import ConnectHandler
    from datetime import datetime

    # pass in device details
    host = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    # setup ssh connection
    net_connect = ConnectHandler(
        device_type='cisco_ios',
        host='192.168.68.10',
        username='admin',
        password='cisco',
        port='22',
        secret='cisco'
    )

    command = 'show ip int brief'
    output = net_connect.send_command(command)

    return render(request, 'index.html', {'details': output})
