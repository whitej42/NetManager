from django.shortcuts import render
from .models import *


# Create your views here.
def index(request):
    devices = Device.objects.all()
    interfaces = Interface.objects.all()
    args = {'devices': devices, 'interfaces': interfaces}
    return render(request, 'index.html', args)
