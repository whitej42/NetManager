from django.template import loader
from django.shortcuts import render


# login views.
def login(request):
    return render(request, 'login.html')


# request account page
def create(request):
    return render(request, 'create.html')
