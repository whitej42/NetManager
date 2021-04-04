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


def index(request):
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
        return redirect('home')

    args = {'form': form}
    messages.warning(request,
                     'Version 0.9 :- The current release of NetManager only supports Cisco devices. Multi-vendor support will be developed in the near future')
    return render(request, 'index.html', args)


# login views.
def sign_in(request):
    next = request.GET.get('next')
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('home')
    args = {'form': form}
    return render(request, 'registration/login.html', args)


# profile view
@login_required
def profile(request):
    profile_form = ProfileForm(request.POST or None, instance=request.user)
    pass_form = ChangePasswordForm(request.POST or None)
    args = {'profile_form': profile_form, 'pass_form': pass_form}
    return render(request, 'profile.html', args)


# update user profile
def update_profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.user.is_authenticated:
        if form.is_valid():
            form.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# change password
def change_password(request):
    form = ChangePasswordForm(request.POST or None, instance=request.user)
    user = User.objects.get(id=request.user.id)
    if request.user.is_authenticated:
        if form.is_valid():
            user.set_password(form.cleaned_data.get('password'))
            user.save()
    return redirect('/')


# delete account
def delete_account(request):
    user_id = request.user.id
    user = User.objects.get(pk=user_id)
    user.delete()
    return redirect('/')
