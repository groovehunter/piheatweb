
from datetime import datetime
from motors.models import Rule

from django.utils import timezone
#now = timezone.now() # TZ aware :)


class BaseRule:
  """ maybe:
      provide access to SensorInfo
  """
  def __init__(self):
    """ common things to do in init. """
    self.now = timezone.now()
    self.DEFAULT_RULE = Rule.objects.get(pk=1)
    print('init base rule', self.__class__.__name__)

  def check(self):
    print('checking')
