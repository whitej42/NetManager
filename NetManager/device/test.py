import os
import json
from dotenv import load_dotenv
from netmiko import ConnectHandler


load_dotenv()

user = os.environ.get('username')
password = os.environ.get('password')
secret = os.environ.get('secret')

router = {
    'device_type': 'cisco_ios',
    'ip': '192.168.68.10',
    'username': 'admin',
    'password': password,
    'secret': secret,
    'port': 22
}

try:
    c = ConnectHandler(**router)
    # store output in python dictionary using TextFSM
    interfaces = c.send_command('show ip int brief', use_textfsm=True)
    for i in interfaces:
        if i['ipaddr'] != 'unassigned':
            output = i
            print(output)
    c.disconnect()
except Exception as e:
    output = e
