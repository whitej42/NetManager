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

def user_input()
    device = input('Choose Device [R1 or R2]: ')
    interface = input('Select Interface: ')
    ip = input('Enter IP Address: ')

def device_connect(host):
    if host == 'R1' or host == 'r1':
        net_connect = ConnectHandler(**R1)
    elif host == 'R2' or host == 'r2':
        net_connect = ConnectHandler(**R2)
    else:
        print('INVALID DEVICE NAME')
        user_input()

    net_connect.enable()
    return net_connect

def configureInterface():
    commands = ['interface ' + interface,
            'ip address ' + ip + ' 255.255.255.0',
            'no shut', 'end',
            'show ip int brief']
    print('\n --------------- Output for ' + 
        net_connect.find_prompt().replace('#',' ') + 
        ' --------------- \n')
    output = net_connect.send_config_set(commands)
    print(output)
    
start = datetime.now()

user_input()
net_connect = device_connect(device)
configureInterface()
net_connect.disconnect()

#confirm changes made
print('\n --------------- Script Complete ---------------')

#print exection time
end = datetime.now()
time = start - end
print('\n Execution Time (secs): ', time.total_seconds())