from django import forms
from device.models import Device


class DeviceForm(forms.ModelForm):
    deviceName = forms.CharField(label='Device Name')
    deviceType = forms.CharField(label='Device Type')
    host = forms.CharField(label='Management Address')
    vendor = forms.CharField(label='Vendor')
    location = forms.CharField(label='Location')
    contact = forms.CharField(label='Contact')

    class Meta:
        model = Device
        fields = [
            'deviceName',
            'deviceType',
            'host',
            'vendor',
            'location',
            'contact',
        ]


class SecurityForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.PasswordInput()
    secret = forms.PasswordInput()

    class Meta:
        model = Device
        fields = [
            'username',
            'password',
            'secret',
        ]
