from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template

from .models import Sensor, Measurement


def index(request):
#    t = get_template('index.html')
    #return HttpResponse("Hello, world. You're at the sensors index.")

    sensors = Sensor.objects.all()
    return render(request, 'sensors/index.html')



def last_measures(request, sensor_id):
    
    
    resp = "You're looking at sensor %s." % sensor_id
    
    #m = Measurement.objects.filter(order_by(dtime))[:20]
    #sensor = Sensor.mea
    return HttpResponse(resp)
