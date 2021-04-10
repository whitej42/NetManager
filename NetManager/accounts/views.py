"""

ACCOUNTS/VIEWS.PY

* INDEX VIEW

* LOGIN VIEW

* PROFILE VIEW

* CHANGE PASSWORD

* REPORTS VIEW

* HELP VIEW

"""

from .forms import *
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from devices.models import Alert
from django.views import View


class IndexView(View):
    template = 'index.html'

    def get(self, request):

        form = RegisterForm()
        args = {'form': form}
        messages.warning(request,
                         'Version 0.9 :- The current release of NetManager only supports Cisco devices. '
                         'Multi-vendor support will be developed in the near future')
        return render(request, self.template, args)

    def post(self, request):
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
        return redirect('devices:Device-Manager')


class LoginView(View):
    template = 'registration/login.html'

    def get(self, request):
        form = LoginForm
        args = {'form': form}
        return render(request, self.template, args)

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
            return redirect('accounts:Index')


class ProfileView(View):
    template = 'accounts_profile.html'
    success_redirect = 'accounts:Profile'

    def get(self, request):
        profile_form = ProfileForm(instance=request.user)
        pass_form = ChangePasswordForm
        args = {'profile_form': profile_form, 'pass_form': pass_form}
        return render(request, self.template, args)

    def post(self, request):

        if 'update' in request.POST:
            form = ProfileForm(request.POST or None, instance=request.user)
            if form.is_valid():
                form.save()
            return redirect(self.success_redirect)

        if 'delete' in request.POST:
            user_id = request.user.id
            user = User.objects.get(pk=user_id)
            user.delete()
            return redirect('/')


# change password
@login_required
def change_password(request):
    form = ChangePasswordForm(request.POST or None, instance=request.user)
    user = User.objects.get(id=request.user.id)
    if form.is_valid():
        user.set_password(form.cleaned_data.get('password'))
        user.save()
        messages.success(request, 'Password Changed Successfully')
        return redirect('/')
    messages.error(request, 'Passwords did not match - Please try again')
    return redirect('accounts:Profile')


class ReportsView(View):
    template = 'accounts_reports.html'

    def get(self, request):
        config_logs = Alert.objects.filter(user__username=request.user)
        args = {'config_logs': config_logs}
        return render(request, self.template, args)


class HelpView(View):
    template = 'accounts_help.html'

    def get(self, request):
        return render(request, self.template)
