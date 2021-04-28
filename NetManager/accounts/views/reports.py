"""

File: devices/views/config.py

Purpose:
    This code is a class based view used to
    render the audit logs

"""
from django.http import HttpResponse
from django.shortcuts import render, redirect
from devices.models import Alert, Backup, Device
from django.views import View
from django.contrib import messages


class ReportsView(View):
    template = 'accounts_reports.html'
    success_redirect = 'accounts:Reports'
    exception_redirect = 'devices:Device-Manager'

    # get audit logs
    def get(self, request):
        audit_logs = Alert.objects.filter(user__username=request.user)
        user_backups = Backup.objects.filter(user__username=request.user)
        args = {'config_logs': audit_logs, 'backups': user_backups}
        return render(request, self.template, args)

    def post(self, request):
        device_id = request.POST.get('device_id')
        device = Device.get_device(device_id)

        # download backup file
        if 'backup' in request.POST:
            backup = Backup.get_device_backup(device)
            response = HttpResponse(backup.file, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename=%s' % backup.file
            return response

        try:
            return redirect(self.success_redirect)
        except Exception as e:
            messages.error(request, 'Unexpected Error - ' + str(e))
            return redirect(self.exception_redirect)