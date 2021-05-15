"""

File: devices/controllers/cisco_controller.py

Purpose:
    This code acts as the controller between the
    application and Cisco devices.

    Functions for retrieving device configuration
    and pushing configuration changes. All functions
    take a device object passed from the views

"""
from netmiko import ConnectHandler
from devices.models import Security
from devices.factory import alert_factory, backup_factory


# establish ssh connection to device
def connect(device):
    device = {
        'device_type': 'cisco_ios',
        'ip': device.host,
        'username': Security.get_username(device),
        'password': Security.get_password(device),
        'secret': Security.get_secret(device),
        'port': 22,
    }
    return device


# retrieve device configuration
def retrieve(device, command):
    try:
        c = ConnectHandler(**connect(device))
        output = c.send_command(command, use_textfsm=True)
        c.disconnect()
    except Exception as e:
        output = e
    return output


# send configuration command to device
def configure(device, command):
    try:
        c = ConnectHandler(**connect(device))
        c.enable()
        c.send_config_set(command)
        c.disconnect()
        return True
    except Exception as e:
        return e


# test connection to all devices
def connect_test(user_devices):
    for i in user_devices:
        try:
            # if connection established
            c = ConnectHandler(**connect(i))
            i.status = True
            c.disconnect()
        except:
            # else device inactive
            i.status = False
        i.save()


# get show ip interface brief output
def get_interfaces(device):
    output = retrieve(device, 'show ip interface brief')
    return output


# get show version output
def get_version(device):
    output = retrieve(device, 'show version')
    return output


# get show ip access-lists output
def get_acl(device):
    output = retrieve(device, 'show ip access-lists')
    return output


# get show interface <interface> output
# i: interface as string
def get_interface_details(device, i):
    output = retrieve(device, 'show interface ' + i)
    return output


# get show ip interface <interface> output
# i: interface as string
def get_interface_ip(device, i):
    output = retrieve(device, 'show ip interface ' + i)
    return output


# save config with Netmiko save_config() function
def save(user, device):
    """
    Another implementation for saving config using the Netmiko
    save_config() function. Broke a few weeks before release

        try:
            c = ConnectHandler(**connect(d))
            c.save_config()
            c.disconnect()
            return alert_factory.save_alert(user, d)
        except Exception as e:
            return str(e)
    """

    # Temporary fix
    cmd = ['copy run start', '']
    c = configure(device, cmd)
    if c:
        return alert_factory.save_alert(user, device)
    else:
        return str(c)


# create new backup file
def backup(user, device):
    try:
        c = ConnectHandler(**connect(device))
        output = c.send_command('show running-config')
        c.disconnect()
        backup_factory.create_backup(device, output)
        return alert_factory.backup_alert(user, device)
    except Exception as e:
        output = e
    return output


# Configure interface with ip address
# form: InterfaceForm
def config_interface(user, device, form):
    intface = form.cleaned_data.get('interface')
    ip = form.cleaned_data.get('ip_address')
    mask = form.cleaned_data.get('mask')
    enable = form.cleaned_data.get('enable')
    if enable:
        cmd = ['interface ' + intface, 'ip address ' + ip + ' ' + mask, 'no shutdown']
    else:
        cmd = ['interface ' + intface, 'ip address ' + ip + ' ' + mask, 'shutdown']
    c = configure(device, cmd)
    if c:
        return alert_factory.configuration_alert(user, device, intface, ip, 'CONFIG')
    else:
        return str(c)


# Reset specific interface to default
# intface: interface as string
def reset_interface(user, device, intface):
    cmd = ['interface ' + intface, 'no ip address', 'shutdown']
    c = configure(device, cmd)
    if c:
        return alert_factory.configuration_alert(user, device, intface, None, 'RESET')
    else:
        return str(c)


# Reset all unused interfaces
def disable_interfaces(user, device):
    interfaces = retrieve(device, 'show ip int brief')
    for i in interfaces:
        if i['ipaddr'] == 'unassigned' and i['status'] != 'administratively down':
            cmd = ['interface ' + i['intf'], 'shutdown']
            configure(device, cmd)
    return True


# Create new access lists & add to access lists
# form = AccessListForm
def create_acl(user, device, form):
    type = form.cleaned_data.get('type')
    name = form.cleaned_data.get('name')
    statement = form.cleaned_data.get('statement')
    cmd = ['ip access-list ' + type + " " + name, statement]
    c = configure(device, cmd)
    if c:
        return alert_factory.security_alert(user, device, name, None, 'CREATE')
    else:
        return str(c)


# Delete access lists from devices
# acl_name: list name as string
def delete_acl(user, device, acl_name):
    cmd = ['no ip access-list ' + acl_name]
    c = configure(device, cmd)
    if c:
        return alert_factory.security_alert(user, device, acl_name, None, 'DELETE')
    else:
        return str(c)


# Apply access list to interface
# intface: interface as string
# acl_name: access list as string
# direction: direction as string
def apply_acl(user, device, intface, acl_name, direction):
    cmd = ['interface ' + intface, 'ip access-group ' + acl_name + ' ' + direction]
    c = configure(device, cmd)
    if c:
        return alert_factory.security_alert(user, device, acl_name, intface, 'APPLY')
    else:
        return str(c)


# Remove access list from interface
# intface: interface as string
# acl_name: access list as string
# direction: direction as string
def remove_acl(user, device, intface, acl_name, direction):
    cmd = ['interface ' + intface, 'no ip access-group ' + acl_name + ' ' + direction]
    c = configure(device, cmd)
    if c:
        return alert_factory.security_alert(user, device, acl_name, intface, 'REMOVE')
    else:
        return str(c)
