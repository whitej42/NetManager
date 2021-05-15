"""

File: accounts/views/index.py

Purpose:
    This code is a class based view used to render
    the index (home page) view.

    Functions allow users to register and create
    a new account

"""
from accounts.forms import *
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View


class IndexView(View):
    template = 'index.html'

    # get template
    def get(self, request):
        form = RegisterForm()
        args = {'form': form}
        messages.warning(request,
                         'Version 0.9 :- The current release of NetManager only supports Cisco devices. '
                         'Multi-vendor support will be developed in the near future')
        return render(request, self.template, args)

    # register new user
    def post(self, request):
        form = RegisterForm(request.POST)
        args = {'form': form}

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            authenticate(username=user.username, password=password)
            login(request, user)

            try:
                messages.success(request,
                                 'Welcome to NetManager! Add new devices to start managing your network. Visit our help page if you get stuck.')
                return redirect('devices:Device-Manager')
            except Exception as e:
                messages.error(request, 'Error: ' + str(e) +
                               ' Please Try Again. If issue persists, contact support')
                return redirect('devices:Device-Manager')

        messages.error(request, 'Error Registering New Account! Rectify Form Errors')
        return render(request, self.template, args)
