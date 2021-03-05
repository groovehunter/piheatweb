from django.db import models


class ControlEvent(models.Model):
  dtime   = models.DateTimeField('dtime of reading, checks and actions', null=True)
  def get_absolute_url(self):
    return self.id
  def __str__(self):
    return self.dtime.strftime('%H-%M-%S')


DEFAULT_EVENT = 1
