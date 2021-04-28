"""

File: devices/factory/backup_factory.py

Purpose:
    This code generates backup files for device configuration
    and saves in the database

"""
from devices.models import Backup


def create_backup(device, backup):
    # save backup file
    b = Backup.objects.get(device=device)
    file = (device.name + '_backup.txt')
    Backup.set_backup(b, file, backup)

