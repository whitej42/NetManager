# DELETE LATER - ONLY FOR REF ATM

import sys
from netmiko import ConnectHandler
from datetime import datetime

# pass in device-manager-manager details
host = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]

# setup ssh connection
net_connect = ConnectHandler(
    device_type='cisco_ios',
    host=host,
    username=username,
    password=password,
    port='22',
    secret='cisco'
)

command = 'show ip int br'

output = net_connect.send_command(command)
print(output)
net_connect.disconnect()