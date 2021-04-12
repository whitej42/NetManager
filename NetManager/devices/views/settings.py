"""

File: devices/views/settings.py

Purpose:
    This code is a class based view used to render
    and provide functions for the device settings view.

    Functions allow users to edit and delete devices
    from the database including the security information

"""
from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect
from devices.forms import *
from devices.models import *
from devices.factory import alert_factory


class DeviceSettings(View):
    template = 'device_settings.html'
    success_redirect = 'devices:Device-Settings'
    exception_redirect = 'device:Device-Manager'

    # get device database information
    # **kwargs = devices primary key
    # returns device settings page
    def get(self, request, **kwargs):
        device_id = self.kwargs['device_id']
        d = Device.get_device(device_id)
        device_form = DeviceForm(instance=d)
        security_form = SecurityForm(instance=Security.get_device_security(device_id))
        args = {'device': d, 'security_form': security_form, 'device_form': device_form}
        return render(request, self.template, args)

    # post device information
    # **kwargs = devices primary key
    # returns device settings page (except 'delete')
    def post(self, request, **kwargs):
        device_id = self.kwargs['device_id']
        d = Device.get_device(device_id)

        # edit device information
        if 'edit' in request.POST:
            form = DeviceForm(request.POST or None, instance=d)
            if form.is_valid():
                d.save()
                alert = alert_generator.device_alert(request.user, d, 'UPDATE')
                messages.success(request, alert)
                return redirect(self.success_redirect, device_id)

        # edit device security information
        if 'security' in request.POST:
            s = Security.get_device_security(device_id)
            form = SecurityForm(request.POST or None, instance=s)
            if form.is_valid():
                s.save()
                alert = alert_generator.device_alert(request.user, s.device, 'SECURITY')
                messages.success(request, alert)
                return redirect(self.success_redirect, device_id)

        # delete device - returns device manager
        if 'delete' in request.POST:
            d.delete()
            alert = alert_generator.device_alert(request.user, d, 'DELETE')
            messages.success(request, alert)
            return redirect('devices:Device-Manager')

        # exception redirect
        return redirect(self.exception_redirect)