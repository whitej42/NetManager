"""

File: devices/factory/alert_factory.py

Purpose:
    This code generates alerts for the audit log based on
    changes made by the device controller and saves in the database

"""
from devices.models import Alert


# configuration saved alert
def save_alert(user, device):
    alert_description = 'Device Configuration Saved'
    Alert.create_alert(user, device.name, 'Configuration', alert_description)
    return alert_description


# new backup alert
def backup_alert(user, device):
    alert_description = 'New Backup Created'
    Alert.create_alert(user, device.name, 'Configuration', alert_description)
    return alert_description


# configuration change alert
def configuration_alert(user, device, interface, ip, action):
    alert_description = None
    if action == 'CONFIG':
        alert_description = (interface + ' configured with IP Address ' + ip)
    if action == 'RESET':
        alert_description = (interface + ' reset and shutdown')
    Alert.create_alert(user, device.name, 'Configuration', alert_description)
    return alert_description


# security changes alert
def security_alert(user, device, acl, interface, action):
    alert_description = None
    if action == 'CREATE':
        alert_description = ('Access list ' + acl + ' created')
    if action == 'DELETE':
        alert_description = ('Access list ' + acl + ' deleted')
    if action == 'APPLY':
        alert_description = ('Access list ' + acl + ' applied to ' + interface)
    if action == 'REMOVE':
        alert_description = ('Access list ' + acl + ' removed from ' + interface)
    if action == 'DISABLE':
        alert_description = 'All unused interfaces shutdown'
    Alert.create_alert(user, device.name, 'Security', alert_description)
    return alert_description


# device database changes alerts
def device_alert(user, device, action):
    alert_description = None
    if action == 'ADD':
        alert_description = ('Device ' + device.name + ' added to device list')
    if action == 'DELETE':
        alert_description = ('Device ' + device.name + ' deleted from device list')
    if action == 'UPDATE':
        alert_description = ('Device ' + device.name + ' settings changed')
    if action == 'SECURITY':
        alert_description = ('Device ' + device.name + ' security settings changed')
    Alert.create_alert(user, device.name, 'Device', alert_description)
    return alert_description
