"""

CONFIGURATOR VIEWS.PY

"""


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from devices import device_controller as controller
from devices .models import Device


# redirect back to page
def refer(PageRequest, message):
    messages.success(PageRequest, message)
    return HttpResponseRedirect(PageRequest.META.get('HTTP_REFERER'))


@login_required
def configurator_view(PageRequest, device_id):
    # get selected devices from db
    try:
        d = Device.get_device(device_id)
        args = {'device': d}
    except Device.DoesNotExist:
        messages.error(PageRequest, 'Invalid URL: Device does not exist')
        return redirect('devices:device-details', device_id)
    return render(PageRequest, 'device_config.html', args)


# always returns /configurator
@login_required
def show_command(PageRequest, device_id):
    d = Device.get_device(device_id)
    cmd = PageRequest.POST.get('txt_show')
    output = controller.retrieve(d, cmd)
    args = {'device': d, 'output': output}
    try:
        return render(PageRequest, 'device_config.html', args)
    except Exception as e:
        return redirect('devices:device-manager')


# always returns /configurator
@login_required
def send_config(PageRequest, device_id):
    d = Device.get_device(device_id)
    config = PageRequest.POST.get('txt_config')
    cmd = config.split("\n")
    controller.configure(d, cmd)
    try:
        return refer(PageRequest, 'Configuration Sent')
    except Exception as e:
        return redirect('devices:device-manager')
