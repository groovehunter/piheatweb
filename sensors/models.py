from django.db import models
from cntrl.models import ControlEvent, DEFAULT_EVENT


UNIT_AVAIL = (
    (u'\xb0C',  'degree Celsius'),
    ('F',       'Fahrenheit'),
)
STEPS332 = 26560
class SensorBase:
  def adc_out_to_resistance(self):
    vsense = (3.3 * self.adc_out) / STEPS332
    r = vsense / ((3.3 - vsense) / 18000 )
    return int(r)


class SensorInfo(models.Model):
    name    = models.CharField(max_length=40)
    descr   = models.CharField(max_length=255)
    unit    = models.CharField(max_length=16)
    thermistor = models.CharField(max_length=32, null=True)
    def get_absolute_url(self):
      return self.id
    def __str__(self):
      return self.name

class SensorData_01(models.Model, SensorBase):
    temperature = models.DecimalField(max_digits=4, decimal_places=2)
    resistance  = models.IntegerField()
    adc_out = models.IntegerField(null=True)
    ctrl_event = models.OneToOneField(ControlEvent,
      on_delete=models.CASCADE,
      default = DEFAULT_EVENT)

class SensorData_02(models.Model, SensorBase):
    temperature = models.DecimalField(max_digits=4, decimal_places=2)
    resistance  = models.IntegerField()
    adc_out = models.IntegerField(null=True)
    ctrl_event = models.OneToOneField(ControlEvent,
      on_delete=models.CASCADE,
      default = DEFAULT_EVENT)

class SensorData_03(models.Model, SensorBase):
    temperature = models.DecimalField(max_digits=4, decimal_places=2)
    resistance  = models.IntegerField()
    adc_out = models.IntegerField(null=True)
    ctrl_event = models.OneToOneField(ControlEvent,
      on_delete=models.CASCADE,
      default = DEFAULT_EVENT)

class SensorData_04(models.Model, SensorBase):
    temperature = models.DecimalField(max_digits=4, decimal_places=2)
    resistance  = models.IntegerField()
    adc_out = models.IntegerField(null=True)
    ctrl_event = models.OneToOneField(ControlEvent,
      on_delete=models.CASCADE,
      default = DEFAULT_EVENT)
