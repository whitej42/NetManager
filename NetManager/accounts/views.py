from django.template import loader
from django.shortcuts import render


# login views.
def login(request):
    return render(request, 'login.html')