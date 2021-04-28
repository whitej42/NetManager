"""

File: devices/views/configurator.py

Purpose:
    This code is a class based view used to render and provide
    functions for the device manual configuration view.

    Functions allow users to send show commands manually to a device
    and send configuration commands manually

"""
from django.contrib import messages
from django.shortcuts import render, redirect
from devices.controllers import cisco_controller as controller
from devices .models import Device
from django.views import View


class DeviceConfig(View):
    template = 'device_config.html'
    success_redirect = 'devices:Device-Config'
    exception_redirect = 'devices:Device-Manager'

    # get device and template
    # **kwargs = devices primary key
    # returns device config page
    def get(self, request, **kwargs):
        device_id = self.kwargs['device_id']
        device = Device.get_device(device_id)
        args = {'device': device}
        return render(request, self.template, args)

    # post show and config commands
    # **kwargs = devices primary key
    # returns device config page
    def post(self, request, **kwargs):
        device_id = self.kwargs['device_id']

        # send show command - return output
        if 'show' in request.POST:
            d = Device.get_device(device_id)
            cmd = request.POST.get('txt_show')
            output = controller.retrieve(d, cmd)
            args = {'device': d, 'output': output}
            return render(request, self.template, args)

        # send configuration
        if 'send' in request.POST:
            d = Device.get_device(device_id)
            config = request.POST.get('txt_config')
            cmd = config.split("\n")
            controller.configure(d, cmd)
            messages.success(request, 'Configuration Sent')
            return redirect(self.success_redirect, device_id)
        return redirect(self.exception_redirect)