import os
import sys
import json
from dotenv import load_dotenv
from netmiko import ConnectHandler

load_dotenv()

# ip = sys.argv[1]
user = os.environ.get('username')
password = os.environ.get('password')
secret = os.environ.get('secret')

# network device
router = {
    'device_type': 'cisco_ios',
    'ip': '192.168.68.10',
    'username': 'admin',
    'password': password,
    'secret': secret,
    'port': 22
}

# open connection & run command
try:
    c = ConnectHandler(**router)
    c.enable()
    # store output in python dictionary using TextFSM
    interfaces = c.send_command('show ip int brief', use_textfsm=True)
    with open('../static/json/interfaces.json', 'w') as f:
        json.dump(interfaces, f, indent=2)
    '''
    # extract set information from command - KEEP FOR REF
    for interface in interfaces:
        if interface['status'] == 'up':
            print(f"Interface: {interface['intf']} IP Address: {interface['ipaddr']}")
    '''
    c.disconnect()
    print('Script Complete')
except Exception as e:
    print(e)
