"""

CONFIGURATOR VIEWS.PY

"""


from django.contrib import messages
from django.shortcuts import render, redirect
from devices import device_controller as controller
from devices .models import Device
from django.views import View


class ConfigView(View):
    template = 'device_config.html'
    success_redirect = 'config:Config'

    def get(self, request, **kwargs):
        device_id = self.kwargs['device_id']
        d = Device.get_device(device_id)
        args = {'device': d}
        return render(request, self.template, args)

    def post(self, request, **kwargs):

        if 'show' in request.POST:
            device_id = self.kwargs['device_id']
            d = Device.get_device(device_id)
            cmd = request.POST.get('txt_show')
            output = controller.retrieve(d, cmd)
            args = {'device': d, 'output': output}
            return render(request, self.template, args)

        if 'send' in request.POST:
            device_id = self.kwargs['device_id']
            d = Device.get_device(device_id)
            config = request.POST.get('txt_config')
            cmd = config.split("\n")
            controller.configure(d, cmd)
            messages.success(request, 'Configuration Sent')
            return redirect(self.success_redirect, device_id)
