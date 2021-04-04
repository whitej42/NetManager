"""

DEVICE FORMS.PY

"""

from django import forms


class InterfaceForm(forms.Form):
    interface = forms.CharField(widget=forms.HiddenInput)
    ip_address = forms.CharField(label="IP Address", widget=forms.TextInput(
        attrs={'class': 'form-control textbox', 'placeholder': 'Enter IP Address'}))
    subnet = forms.CharField(label="IP Address", widget=forms.TextInput(
        attrs={'class': 'form-control textbox', 'placeholder': 'Enter Subnet Mask'}))
    enable = forms.BooleanField(label='Enable Interface', required=False, initial=True)


class AclForm(forms.Form):
    type_choices = [('standard', 'Standard'), ('extended', 'Extended')]

    type = forms.CharField(label='Access List Type', widget=forms.Select(choices=type_choices, attrs={'class': 'form-control'}))
    name = forms.CharField(label='Access List Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Access List Name'}))
    statement = forms.CharField(label='Access List Command', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. permit tcp any any'}))


class ApplyAclForm(forms.Form):
    dir_choices = [('in', 'In'), ('out', 'Out')]

    interface = forms.CharField()
    access_list = forms.CharField(label='Select Access List', widget=forms.Select(attrs={'class': 'form-control'}))
    direction = forms.CharField(label='Select Direction', widget=forms.Select(choices=dir_choices, attrs={'class': 'form-control'}))
