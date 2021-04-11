"""

File: devices/views/configurator.py

Purpose:
    This code is a class based view used to render and provide
    functions for the account profile view.

    Functions allow users to view and edit their account information
    and change their password

"""
from accounts.forms import *
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View


class ProfileView(View):
    template = 'accounts_profile.html'
    success_redirect = 'accounts:Profile'

    # get account information
    # returns profile page
    def get(self, request):
        profile_form = ProfileForm(instance=request.user)
        pass_form = ChangePasswordForm
        args = {'profile_form': profile_form, 'pass_form': pass_form}
        return render(request, self.template, args)

    # post account information
    # returns profile page (except 'delete')
    def post(self, request):
        # edit user details
        if 'update' in request.POST:
            form = ProfileForm(request.POST or None, instance=request.user)
            if form.is_valid():
                form.save()
            return redirect(self.success_redirect)

        # delete user account
        # returns index page
        if 'delete' in request.POST:
            user_id = request.user.id
            user = User.objects.get(pk=user_id)
            user.delete()
            return redirect('/')
        # exception redirect
        return redirect('/')


# change password function based view
# returns index page
@login_required
def change_password(request):
    form = ChangePasswordForm(request.POST or None, instance=request.user)
    user = User.objects.get(id=request.user.id)
    if form.is_valid():
        user.set_password(form.cleaned_data.get('password'))
        user.save()
        messages.success(request, 'Password Changed Successfully')
        return redirect('/')
    # if form not valid
    messages.error(request, 'Passwords did not match - Please try again')
    return redirect('accounts:Profile')