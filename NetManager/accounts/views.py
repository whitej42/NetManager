"""

ACCOUNTS VIEW.PY
* HOME PAGE
    * ACCOUNT MANAGEMENT
    * ACCOUNT AUTHENTICATION

"""

from .forms import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from devices.models import Alert


def index_view(request):
    next = request.GET.get('next')
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        authenticate(username=user.username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('devices:device-list')

    args = {'form': form}
    messages.warning(request,
                     'Version 0.9 :- The current release of NetManager only supports Cisco devices. Multi-vendor support will be developed in the near future')
    return render(request, 'index.html', args)


# login views.
def login_view(request):
    next = request.GET.get('next')
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('misc')
    args = {'form': form}
    return render(request, 'registration/login.html', args)


# profile view
@login_required
def profile_view(request):
    profile_form = ProfileForm(request.POST or None, instance=request.user)
    pass_form = ChangePasswordForm(request.POST or None)
    args = {'profile_form': profile_form, 'pass_form': pass_form}
    return render(request, 'accounts_profile.html', args)


# update user profile
@login_required
def update_profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# change password
@login_required
def change_password(request):
    form = ChangePasswordForm(request.POST or None, instance=request.user)
    user = User.objects.get(id=request.user.id)
    if form.is_valid():
        user.set_password(form.cleaned_data.get('password'))
        user.save()
    return redirect('/')


# delete account
@login_required
def delete_account(request):
    user_id = request.user.id
    user = User.objects.get(pk=user_id)
    user.delete()
    return redirect('/')


# reports view
@login_required
def reports_view(PageRequest):
    config_logs = Alert.objects.filter(user__username=PageRequest.user)
    args = {'config_logs': config_logs}
    return render(PageRequest, 'accounts_reports.html', args)


# help page view
def help_view(request):
    return render(request, 'accounts_help.html')
