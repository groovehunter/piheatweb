from django.db import models


class Sensor(models.Model):
    
    name    = models.CharField(max_length=16)
    descr   = models.CharField(max_length=255)
    


class Measurement(models.Model):
    
        
    sensor  = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    dtime   = models.DateTimeField('date published')
    value   = models.IntegerField()
    