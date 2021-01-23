from django.db import models



UNIT_AVAIL = (
    (u'\xb0C',  'degree Celsius'),
    ('F',       'Fahrenheit'),
)

class SensorBase:
  def adc_out_to_resistance(self):
    vsense = (3.3 * self.adc_out) / 26110
    r = vsense / ((3.3 - vsense) / 18000 )
    return r


class SensorInfo(models.Model):
    name    = models.CharField(max_length=40)
    descr   = models.CharField(max_length=255)
    unit    = models.CharField(max_length=16)
    thermistor = models.CharField(max_length=32, null=True)
    def get_absolute_url(self):
      return self.id

class SensorData_01(models.Model, SensorBase):
    dtime   = models.DateTimeField('datetime of measurement')
    temperature = models.DecimalField(max_digits=4, decimal_places=2)
    resistance  = models.IntegerField()
    adc_out = models.IntegerField(null=True)

class SensorData_02(models.Model, SensorBase):
    dtime   = models.DateTimeField('date of measurement')
    temperature = models.DecimalField(max_digits=4, decimal_places=2)
    resistance  = models.IntegerField()
    adc_out = models.IntegerField(null=True)

class SensorData_03(models.Model, SensorBase):
    dtime   = models.DateTimeField('date of measurement')
    temperature = models.DecimalField(max_digits=4, decimal_places=2)
    resistance  = models.IntegerField()
    adc_out = models.IntegerField(null=True)

class SensorData_04(models.Model, SensorBase):
    dtime   = models.DateTimeField('date of measurement')
    temperature = models.DecimalField(max_digits=4, decimal_places=2)
    resistance  = models.IntegerField()
    adc_out = models.IntegerField(null=True)


class ReadingEvent(models.Model):
  dtime   = models.DateTimeField('date of measurement')
  sid01 = models.ForeignKey(SensorData_01, on_delete=models.CASCADE, null=True)
  sid02 = models.ForeignKey(SensorData_02, on_delete=models.CASCADE, null=True)
  sid03 = models.ForeignKey(SensorData_03, on_delete=models.CASCADE, null=True)
  sid04 = models.ForeignKey(SensorData_04, on_delete=models.CASCADE, null=True)
