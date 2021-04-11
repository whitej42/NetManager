"""

File: devices/views/configurator.py

Purpose:
    This code is a class based view used to
    render the audit logs


"""
from django.shortcuts import render
from devices.models import Alert
from django.views import View


class ReportsView(View):
    template = 'accounts_reports.html'

    # get audit logs
    def get(self, request):
        audit_logs = Alert.objects.filter(user__username=request.user)
        args = {'config_logs': audit_logs}
        return render(request, self.template, args)
