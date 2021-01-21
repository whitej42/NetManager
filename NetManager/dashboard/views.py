from django.shortcuts import render
from .models import *
from subprocess import run, PIPE
import sys


def index(request):
    devices = Device.objects.all()
    args = {'devices': devices}
    return render(request, 'index.html', args)
