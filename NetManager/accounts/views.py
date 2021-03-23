from .forms import LoginForm, RegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model, login, logout


def index(request):
    next = request.GET.get('next')
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('dashboard', username=user.username)

    args = {'form': form}
    return render(request, 'index.html', args)


# login views.
def signin(request):
    next = request.GET.get('next')
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('dashboard', username=username)
    args = {'form': form}
    return render(request, 'registration/login.html', args)