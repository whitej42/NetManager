#Basic Show Command Test using Nekmiko SSH
#Connect to a device and configure ip address on an interface

from netmiko import ConnectHandler
from datetime import datetime

#router 1
R1 = {
    'device_type': 'cisco_ios',
    'host': '192.168.146.130',
    'username': 'admin',
    'password': 'cisco',
    'port': '22',
}

#router 2
R2 = {
    'device_type': 'cisco_ios',
    'host': '192.168.147.130',
    'username': 'admin',
    'password': 'cisco',
    'port': '22',
}

def device_connect(host):
    if host == 'R1':
        net_connect = ConnectHandler(**R1)
    else:
        net_connect = ConnectHandler(**R2)

    net_connect.enable()
    return net_connect

def configureInterface():
    commands = ['int ' + interface,
            'ip address ' + ip + ' 255.255.255.0',
            'no shut', 'end',
            'show ip int brief']
    print('\n --------------- Output for ' + 
        net_connect.find_prompt().replace('#',' ') + 
        ' --------------- \n')
    output = net_connect.send_config_set(commands)
    print(output)
    
device = input('Choose Device [R1 or R2]: ')
interface = input('Select Interface: ')
ip = input('Enter IP Address: ')

start = datetime.now()

net_connect = device_connect(device)
configureInterface()
net_connect.disconnect()

#confirm changes made
print('\n --------------- Script Complete ---------------')

#print exection time
end = datetime.now()
time = start - end
print('\n Execution Time (secs): ', time.total_seconds())