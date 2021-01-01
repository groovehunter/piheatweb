from django.db import models


class SensorBase(models.Model): 
    UNIT_AVAIL = (
        (u'\xb0C',  'degree Celsius'),
        ('F',       'Fahrenheit'),
    )


class SensorInfo(models.Model):
    name    = models.CharField(max_length=16)
    descr   = models.CharField(max_length=255)
    unit    = models.CharField(max_length=16)
    pin_bcm = models.IntegerField()
    

class SensorData_01(SensorBase):
    dtime   = models.DateTimeField('date of measurement')
    temperature = models.DecimalField(max_digits=4, decimal_places=2)
    resistance  = models.IntegerField()
    
class SensorData_02(SensorBase):
    dtime   = models.DateTimeField('date of measurement')
    temperature = models.DecimalField(max_digits=4, decimal_places=2)
    resistance  = models.IntegerField()
    
class SensorData_03(SensorBase):
    dtime   = models.DateTimeField('date of measurement')
    temperature = models.DecimalField(max_digits=4, decimal_places=2)
    resistance  = models.IntegerField()
    
class SensorData_04(SensorBase):
    dtime   = models.DateTimeField('date of measurement')
    temperature = models.DecimalField(max_digits=4, decimal_places=2)
    resistance  = models.IntegerField()
    

