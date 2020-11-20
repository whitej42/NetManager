from django.template import loader
from django.http import HttpResponse


# login views.
def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render({}, request))


# request account page
def create(request):
    template = loader.get_template('create.html')
    return HttpResponse(template.render({}, request))
