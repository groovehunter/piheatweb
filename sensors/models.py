from django.db import models


class SensorBase: pass

UNIT_AVAIL = (
    (u'\xb0C',  'degree Celsius'),
    ('F',       'Fahrenheit'),
)


class SensorInfo(models.Model):
    name    = models.CharField(max_length=40)
    descr   = models.CharField(max_length=255)
    unit    = models.CharField(max_length=16)

    def get_absolute_url(self):
      return self.id

class SensorData_01(models.Model, SensorBase):
    dtime   = models.DateTimeField('date of measurement')
    temperature = models.DecimalField(max_digits=4, decimal_places=2)
    resistance  = models.IntegerField()

class SensorData_02(models.Model, SensorBase):
    dtime   = models.DateTimeField('date of measurement')
    temperature = models.DecimalField(max_digits=4, decimal_places=2)
    resistance  = models.IntegerField()

class SensorData_03(models.Model, SensorBase):
    dtime   = models.DateTimeField('date of measurement')
    temperature = models.DecimalField(max_digits=4, decimal_places=2)
    resistance  = models.IntegerField()

class SensorData_04(models.Model, SensorBase):
    dtime   = models.DateTimeField('date of measurement')
    temperature = models.DecimalField(max_digits=4, decimal_places=2)
    resistance  = models.IntegerField()
