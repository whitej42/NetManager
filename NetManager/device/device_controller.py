"""

CISCO DEVICE CONTROLLER

"""

from netmiko import ConnectHandler
from .models import Security


def connect(d):
    device = {
        'device_type': 'cisco_ios',
        'ip': d.host,
        'username': Security.get_username(d),
        'password': Security.get_password(d),
        'secret': Security.get_secret(d),
        'port': 22,
    }
    return device


# retrieve device information
def retrieve(device, command):
    try:
        c = ConnectHandler(**connect(device))
        output = c.send_command(command, use_textfsm=True)
        c.disconnect()
    except Exception as e:
        output = e
    return output


# send configuration to device
def configure(d, command):
    try:
        c = ConnectHandler(**connect(d))
        c.enable()
        c.send_config_set(command)
        c.disconnect()
        return True
    except Exception as e:
        return e


# test connection to all devices
def connect_test(user_devices):
    for i in user_devices:  # hard-coded - CHANGE THIS!!
        try:
            # if connection established
            c = ConnectHandler(**connect(i))
            i.status = True
            c.disconnect()
        except:
            i.status = False
        i.save()


# save config with Netmiko save_config() function
def save_config(d):
    try:
        c = ConnectHandler(**connect(d))
        c.save_config()
        c.disconnect()
        return 'Configuration Saved'
    except Exception as e:
        return str(e)


# get show ip interface brief output
# d = device object
def get_interfaces(d):
    output = retrieve(d, 'show ip interface brief')
    return output


# get show version output
# d = device object
def get_version(d):
    output = retrieve(d, 'show version')
    return output


# get show ip access-lists output
# d = device object
def get_acl(d):
    output = retrieve(d, 'show ip access-lists')
    return output


# get show interface <interface> output
# d = device object
# i = interface as string
def get_interface_details(d, i):
    output = retrieve(d, 'show interface ' + i)
    return output


# get show ip interface <interface> output
# d = device object
# i = interface as string
def get_interface_ip(d, i):
    output = retrieve(d, 'show ip interface ' + i)
    return output


# Configure interface with ip address
# d = device object
# form = InterfaceForm
def config_interface(d, form):
    current_interface = form.cleaned_data.get('interface')
    address = form.cleaned_data.get('ip_address')
    subnet = form.cleaned_data.get('subnet')
    enable = form.cleaned_data.get('enable')
    if enable:
        cmd = ['interface ' + current_interface, 'ip address ' + address + ' ' + subnet, 'no shutdown']
    else:
        cmd = ['interface ' + current_interface, 'ip address ' + address + ' ' + subnet, 'shutdown']
    return configure(d, cmd)


# Reset specific interface to default
# d = device object
# i = interface as string
def reset_interface(d, i):
    cmd = ['interface ' + i, 'no ip address', 'shutdown']
    return configure(d, cmd)


# Reset all unused interfaces
# d = device object
def disable_interfaces(d):
    interfaces = retrieve(d, 'show ip int brief')
    for i in interfaces:
        if i['ipaddr'] == 'unassigned' and i['status'] != 'administratively down':
            cmd = ['interface ' + i['intf'], 'shutdown']
            configure(d, cmd)
    return True


# Configure new access lists & add to access lists
# d = device object
# form=AccessListForm
def configure_acl(d, form):
    acl_type = form.cleaned_data.get('type')
    name = form.cleaned_data.get('name')
    acl = form.cleaned_data.get('statement')
    cmd = ['ip access-list ' + acl_type + " " + name, acl]
    return configure(d, cmd)


# Delete access lists from device
# d = device object
# acl = list name as string
def delete_acl(d, acl):
    cmd = ['no ip access-list ' + acl]
    return configure(d, cmd)


# Apply access list to interface
# d = device object
# i = interface as string
# acl = access list as string
# direction = direction as string
def apply_acl(d, i, acl, direction):
    cmd = ['interface ' + i, 'ip access-group ' + acl + ' ' + direction]
    return configure(d, cmd)


# Remove access list from interface
# d = device object
# i = interface as string
# acl = access list as string
# direction = direction as string
def remove_acl(d, i, acl, direction):
    cmd = ['interface ' + i, 'no ip access-group ' + acl + ' ' + direction]
    return configure(d, cmd)