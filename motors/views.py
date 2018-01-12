from django.shortcuts import render
from django.template import RequestContext

from .models import Motor



def index(request):

    motors = Motor.objects.all()
    c = RequestContext(request)
    c['entries'] = motors
    return render(request, 'index.html')


