"""

File: devices/views/interface.py

Purpose:
    This code is a class based view used to render
    and provide functions for the interface details view.

    Functions allow users to view interface configuration,
    apply and remove access lists from an interface

"""
from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect
from devices.controllers import device_controller as controller
from devices.models import *


class InterfaceDetails(View):
    template = 'device_interface.html'
    success_redirect = 'devices:Interface-Details'
    exception_redirect = 'device:Device-Manager'

    # get interface configuration
    # **kwargs = devices primary key
    # returns interface details page
    def get(self, request, **kwargs):
        device_id = self.kwargs['device_id']
        i = self.kwargs['interface']
        d = Device.get_device(device_id)
        args = {'device': d, 'interface': i, 'details': controller.get_interface_details(d, i),
                'int_acl': controller.get_interface_ip(d, i), 'acl': controller.get_acl(d)}
        return render(request, self.template, args)

    # post interface configuration
    # **kwargs = devices primary key
    # returns interface details page
    def post(self, request, **kwargs):

        device_id = self.kwargs['device_id']
        i = self.kwargs['interface']
        d = Device.get_device(device_id)

        # apply access list to interface
        if 'apply' in request.POST:
            # poor form implementation
            acl = request.POST.get('acl')
            direction = request.POST.get('dir')
            c = controller.apply_acl(request.user, d, i, acl, direction)
            messages.success(request, str(c))
            return redirect(self.success_redirect, device_id, i)

        # remove access list from interface
        if 'remove' in request.POST:
            # poor form implementation
            acl = request.POST.get('acl')
            direction = request.POST.get('dir')
            c = controller.remove_acl(request.user, d, i, acl, direction)
            messages.success(request, str(c))
            return redirect(self.success_redirect, device_id, i)

        return redirect(self.exception_redirect)
