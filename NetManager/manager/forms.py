from django import forms
from .models import Device


class DeviceForm(forms.ModelForm):
    device = forms.CharField(label='Device Name')
    deviceType = forms.CharField(label='Device Type')
    host = forms.CharField(label='Management Address')
    vendor = forms.CharField(label='Vendor')
    location = forms.CharField(label='Location')
    contact = forms.CharField(label='Contact')

    class Meta:
        model = Device
        fields = [
            'device',
            'deviceType',
            'host',
            'vendor',
            'location',
            'contact'
        ]