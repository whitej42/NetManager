from django.shortcuts import render


# device manager view
def device_manager(request):
    return render(request, 'manager.html')
