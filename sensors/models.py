from django.db import models


class Sensor(models.Model):
    
    UNIT_AVAIL = (
        (u'\xb0C',  'degree Celsius'),
        ('F',       'Fahrenheit'),
    )
    name    = models.CharField(max_length=16)
    descr   = models.CharField(max_length=255)
    unit    = models.CharField(max_length=16)
    


class Measurement(models.Model):
        
    sensor  = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    dtime   = models.DateTimeField('date published')
    value   = models.DecimalField(max_digits=4, decimal_places=2)
    