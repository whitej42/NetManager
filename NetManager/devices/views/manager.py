"""

File: devices/views/manager.py

Purpose:
    This code is a class based view used to render and provide
    functions for the device manager view.

    Functions allow users to view their devices and add new devices.

"""
import datetime
from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect
from devices.factory import alert_factory
from devices.controllers import cisco_controller as controller
from devices.forms import *
from devices.models import *


class DeviceManager(View):
    form_class = DeviceForm
    template = 'device_manager.html'
    success_redirect = 'devices:Device-Manager'
    exception_redirect = 'accounts.Index'

    # get user devices & audit logs/24hrs
    # returns device manager view
    def get(self, request):
        form = self.form_class()
        user_devices = Device.objects.filter(user__username=request.user)
        date = datetime.datetime.now() - datetime.timedelta(days=1)
        audit_logs = Alert.objects.filter(user__username=request.user, date__gt=date)

        args = {'devices': user_devices, 'status': controller.connect_test(user_devices),
                'audit_logs': audit_logs, 'form': form}
        try:
            return render(request, self.template, args)
        except Exception as e:
            messages.error(request, 'Error - ' + str(e))
            return redirect(self.exception_redirect)

    # post new device
    # returns device manager view
    def post(self, request):
        user = User.objects.get(username=request.user)
        form = self.form_class(request.POST or None)
        if form.is_valid():
            d = form.save(commit=False)
            d.user = user
            d.save()
            Security.create_blank_security(d)
            alert = alert_factory.device_alert(request.user, d, 'ADD')
            messages.success(request, alert + " - Remember! Add login credentials in the device settings")

        try:
            return redirect(self.success_redirect)
        except Exception as e:
            messages.error(request, 'Error - ' + str(e))
            return redirect(self.exception_redirect)
