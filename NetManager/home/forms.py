from django import forms
from device.models import Device, Security


class DeviceForm(forms.ModelForm):
    vendor_choices = [('cisco_ios', 'Cisco')]

    name = forms.CharField(label="Device Name", widget=forms.TextInput(attrs={'class': 'form-control textbox edit', 'disabled': 'true'}))
    type = forms.CharField(label="Device Type", widget=forms.TextInput(attrs={'class': 'form-control textbox edit', 'disabled': 'true'}))
    host = forms.CharField(label="SSH Address", widget=forms.TextInput(attrs={'class': 'form-control textbox edit', 'disabled': 'true'}))
    vendor = forms.CharField(label='Access List Type', widget=forms.Select(choices=vendor_choices, attrs={'class': 'form-control', 'disabled': 'true'}))
    location = forms.CharField(label="Location", widget=forms.TextInput(attrs={'class': 'form-control textbox edit', 'disabled': 'true'}))
    contact = forms.CharField(label='Contact', widget=forms.TextInput(attrs={'class': 'form-control textbox edit', 'disabled': 'true'}))

    class Meta:
        model = Device
        fields = [
            'name',
            'type',
            'host',
            'vendor',
            'location',
            'contact',
        ]


class SecurityForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control textbox security', 'disabled': 'true'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control textbox security', 'disabled': 'true'}))
    secret = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control textbox security', 'disabled': 'true'}))

    class Meta:
        model = Security
        fields = [
            'username',
            'password',
            'secret',
        ]
