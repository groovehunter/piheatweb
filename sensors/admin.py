from django.contrib import admin

from .models import Sensor
from .models import Measurement

admin.site.register(Measurement)
admin.site.register(Sensor)