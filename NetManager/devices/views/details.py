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
        device = Device.get_device(device_id)
        int_form = InterfaceForm
        acl_form = AclForm
        args = {'device': device, 'int_form': int_form, 'acl_form': acl_form,
                'interfaces': controller.get_interfaces(device),
                'version': controller.get_version(device),
                'acl': controller.get_acl(device)}
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
        device = Device.get_device(device_id)

        # save device configuration
        if 'save' in request.POST:
            save = controller.save(request.user, device)
            messages.success(request, save)

        # backup device configuration
        if 'backup' in request.POST:
            backup = controller.backup(request.user, device)
            messages.success(request, backup)

        # save and backup device config
        if 'full' in request.POST:
            controller.save(request.user, device)
            controller.backup(request.user, device)
            messages.success(request, 'Device Configuration Saved and New Backup Created')

        # configure interface ip address
        if 'config' in request.POST:
            form = InterfaceForm(request.POST or None)
            if form.is_valid():
                c = controller.config_interface(request.user, device, form)
                messages.success(request, str(c))

        # reset interface
        if 'reset' in request.POST:
            intface = request.POST.get('reset')
            c = controller.reset_interface(request.user, device, intface)
            messages.success(request, str(c))

        # disable all unused interfaces
        if 'disable' in request.POST:
            c = controller.disable_interfaces(request.user, device)
            messages.success(request, str(c))

        # create new access list
        if 'create' in request.POST:
            form = AclForm(request.POST or None)
            if form.is_valid():
                c = controller.create_acl(request.user, device, form)
                messages.success(request, str(c))

        # delete access list
        if 'delete' in request.POST:
            acl = request.POST.get('acl')
            c = controller.delete_acl(request.user, device, acl)
            messages.success(request, str(c))

        try:
            return redirect(self.success_redirect, device_id)
        except Exception as e:
            messages.error(request, 'Unexpected Error - ' + str(e))
            return redirect(self.exception_redirect)
