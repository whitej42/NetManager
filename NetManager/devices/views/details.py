"""

File: accounts/views/details.py

Purpose:
    This code is a class based view used to render
    and provide functions for the device details view.

    Functions allow users to view and save device
    configuration, configure and reset interfaces,
    disable interfaces, create and delete access lists.

"""
from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect
from devices.controllers import cisco_controller as controller
from devices.forms import *
from devices.models import *


class DeviceDetails(View):
    template = 'device_details.html'
    success_redirect = 'devices:Device-Details'
    exception_redirect = 'devices:Device-Manager'

    # get device configuration & config
    # **kwargs = devices primary key
    # returns device details page
    def get(self, request, **kwargs):
        device_id = self.kwargs['device_id']
        d = Device.get_device(device_id)
        int_form = InterfaceForm
        acl_form = AclForm
        args = {'device': d, 'int_form': int_form, 'acl_form': acl_form, 'interfaces': controller.get_interfaces(d),
                'version': controller.get_version(d), 'acl': controller.get_acl(d)}
        try:
            return render(request, self.template, args)
        except Exception as e:
            messages.error(request, 'Error - ' + str(e))
            return redirect(self.exception_redirect)

    # post device configuration
    # **kwargs = devices primary key
    # returns device details page
    def post(self, request, **kwargs):
        device_id = self.kwargs['device_id']
        d = Device.get_device(device_id)

        # save device configuration
        if 'save' in request.POST:
            save = controller.save_config(request.user, d)
            messages.success(request, save)

        # configure interface ip address
        if 'config' in request.POST:
            form = InterfaceForm(request.POST or None)
            if form.is_valid():
                c = controller.config_interface(request.user, d, form)
                messages.success(request, str(c))

        # reset interface
        if 'reset' in request.POST:
            i = request.POST.get('reset')
            c = controller.reset_interface(request.user, d, i)
            messages.success(request, str(c))

        # disable all unused interfaces
        if 'disable' in request.POST:
            c = controller.disable_interfaces(request.user, d)
            messages.success(request, str(c))

        # create new access list
        if 'create' in request.POST:
            form = AclForm(request.POST or None)
            if form.is_valid():
                c = controller.create_acl(request.user, d, form)
                messages.success(request, str(c))

        # delete access list
        if 'delete' in request.POST:
            acl = request.POST.get('acl')
            c = controller.delete_acl(request.user, d, acl)
            messages.success(request, str(c))

        try:
            return redirect(self.success_redirect, device_id)
        except Exception as e:
            messages.error(request, 'Error - ' + str(e))
            return redirect(self.exception_redirect)
