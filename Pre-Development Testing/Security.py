import netmiko
from netmiko import ConnectHandler

device = {
        'device_type': 'cisco_ios',
        'ip': '192.168.0.30',
        'username': 'admin',
        'password': 'cisco',
        'secret': 'cisco',
        'port': 22
    }


c = ConnectHandler(**device)
c.enable()

def login_banner():
	banner =  input ("Enter a banner: ")
	n = len(banner) + 2
	border = '*' * n
	c.send_command('banner login ^')
	c.send_command(border)
	c.send_command(' ' + banner)
	c.send_command(border + '^')

# Shutdown unused interfaces
def disable_interfaces():
	interfaces = c.send_command('show ip int brief', use_textfsm=True)

	for interface in interfaces:
		if interface['ipaddr'] == 'unassigned' and interface['status'] != 'administratively down':
			commands = ['interface ' + interface['intf'],'shutdown']
			c.send_config_set(commands)


login_banner()
c.disconnect()
print('Script Complete')
