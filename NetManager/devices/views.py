"""

Devices Class Based Views

"""
import datetime
from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect
from devices import device_controller as controller
from devices.forms import *
from devices.models import *
from devices import alert_generator

'''
Device Manager Class Based View
'''


class DeviceManager(View):
    form_class = DeviceForm
    template = 'device_manager.html'
    success_redirect = 'devices:Device-Manager'
    exception_redirect = 'accounts.Index'

    def get(self, request):
        form = self.form_class()
        user_devices = Device.objects.filter(user__username=request.user)
        date = datetime.datetime.now() - datetime.timedelta(days=1)
        config_logs = Alert.objects.filter(user__username=request.user, date__gt=date)

        args = {'devices': user_devices, 'status': controller.connect_test(user_devices),
                'config_logs': config_logs, 'form': form}
        return render(request, self.template, args)

    def post(self, request):

        # add device
        user = User.objects.get(username=request.user)
        form = self.form_class(request.POST or None)
        if form.is_valid():
            d = form.save(commit=False)
            d.user = user
            d.save()
            Security.create_blank_security(d)
            alert = alert_generator.device_alert(request.user, d, 'ADD')
            messages.success(request, alert)
            return redirect(self.success_redirect)
        return redirect(self.exception_redirect)


''' 
Device Details Class Based View
'''


class DeviceDetails(View):
    template = 'device_details.html'
    success_redirect = 'devices:Device-Details'
    exception_redirect = 'device:Device-Manager'

    def get(self, request, **kwargs):
        device_id = self.kwargs['device_id']
        d = Device.get_device(device_id)
        int_form = InterfaceForm
        acl_form = AclForm
        args = {'device': d, 'int_form': int_form, 'acl_form': acl_form, 'interfaces': controller.get_interfaces(d),
                'version': controller.get_version(d), 'acl': controller.get_acl(d)}
        return render(request, self.template, args)

    def post(self, request, **kwargs):
        device_id = self.kwargs['device_id']
        d = Device.get_device(device_id)

        if 'save' in request.POST:
            save = controller.save_config(request.user, d)
            messages.success(request, save)
            return redirect(self.success_redirect, device_id)

        if 'config' in request.POST:
            form = InterfaceForm(request.POST or None)
            if form.is_valid():
                c = controller.config_interface(request.user, d, form)
                messages.success(request, str(c))
                return redirect(self.success_redirect, device_id)

        if 'reset' in request.POST:
            i = request.POST.get('reset')
            c = controller.reset_interface(request.user, d, i)
            messages.success(request, str(c))
            return redirect(self.success_redirect, device_id)

        if 'disable' in request.POST:
            c = controller.disable_interfaces(request.user, d)
            messages.success(request, str(c))
            return redirect(self.success_redirect, device_id)

        if 'create' in request.POST:
            form = AclForm(request.POST or None)
            if form.is_valid():
                c = controller.create_acl(request.user, d, form)
                messages.success(request, str(c))
                return redirect(self.success_redirect, device_id)

        if 'delete' in request.POST:
            acl = request.POST.get('acl')
            c = controller.delete_acl(request.user, d, acl)
            messages.success(request, str(c))
            return redirect(self.success_redirect, device_id)

        return redirect(self.exception_redirect)


"""
Interface Details Class Based View
"""


class InterfaceDetails(View):
    template = 'device_interface.html'
    success_redirect = 'devices:Interface-Details'
    exception_redirect = 'device:Device-Manager'

    def get(self, request, **kwargs):
        device_id = self.kwargs['device_id']
        i = self.kwargs['interface']
        d = Device.get_device(device_id)
        args = {'device': d, 'interface': i, 'details': controller.get_interface_details(d, i),
                'int_acl': controller.get_interface_ip(d, i), 'acl': controller.get_acl(d)}
        return render(request, self.template, args)

    def post(self, request, **kwargs):

        device_id = self.kwargs['device_id']
        i = self.kwargs['interface']
        d = Device.get_device(device_id)

        if 'apply' in request.POST:
            # poor form implementation
            acl = request.POST.get('acl')
            direction = request.POST.get('dir')
            c = controller.apply_acl(request.user, d, i, acl, direction)
            messages.success(request, str(c))
            return redirect(self.success_redirect, device_id, i)

        if 'remove' in request.POST:
            # poor form implementation
            acl = request.POST.get('acl')
            direction = request.POST.get('dir')
            c = controller.remove_acl(request.user, d, i, acl, direction)
            messages.success(request, str(c))
            return redirect(self.success_redirect, device_id, i)

        return redirect(self.exception_redirect)


''' 

Device Settings Class Based View

'''


class DeviceSettings(View):
    template = 'device_settings.html'
    success_redirect = 'devices:Device-Settings'
    exception_redirect = 'device:Device-Manager'

    def get(self, request, **kwargs):
        device_id = self.kwargs['device_id']
        d = Device.get_device(device_id)
        device_form = DeviceForm(instance=d)
        security_form = SecurityForm(instance=Security.get_device_security(device_id))
        args = {'device': d, 'security_form': security_form, 'device_form': device_form}
        return render(request, self.template, args)

    def post(self, request, **kwargs):
        device_id = self.kwargs['device_id']
        d = Device.get_device(device_id)

        if 'edit' in request.POST:
            form = DeviceForm(request.POST or None, instance=d)
            if form.is_valid():
                d.save()
                alert = alert_generator.device_alert(request.user, d, 'UPDATE')
                messages.success(request, alert)
                return redirect(self.success_redirect, device_id)

        if 'security' in request.POST:
            s = Security.get_device_security(device_id)
            form = SecurityForm(request.POST or None, instance=s)
            if form.is_valid():
                s.save()
                alert = alert_generator.device_alert(request.user, s.device, 'SECURITY')
                messages.success(request, alert)
                return redirect(self.success_redirect, device_id)

        if 'delete' in request.POST:
            d.delete()
            alert = alert_generator.device_alert(request.user, d, 'DELETE')
            messages.success(request, alert)
            return redirect('devices:Device-Manager')

        return redirect(self.exception_redirect)