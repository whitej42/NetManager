"""

File: devices/views/configurator.py

Purpose:
    This code is a class based view used to render
    the login page

    Functions for logging in users

"""
from accounts.forms import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View


class LoginView(View):
    template = 'registration/login.html'

    # get template
    def get(self, request):
        form = LoginForm
        args = {'form': form}
        return render(request, self.template, args)

    # authenticate and log in
    def post(self, request):
        next = request.GET.get('next')
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            if next:
                return redirect(next)
            return redirect('devices:Device-Manager')