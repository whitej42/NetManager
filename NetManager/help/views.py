from django.shortcuts import render


# help page view
def help_page(request):
    return render(request, 'help.html')