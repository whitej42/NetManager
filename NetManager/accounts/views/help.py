"""

File: accounts/views/help.py

Purpose:
    This code is a class based view used to render
    the help page


"""
from django.shortcuts import render
from django.views import View


class HelpView(View):
    template = 'accounts_help.html'

    def get(self, request):
        return render(request, self.template)
