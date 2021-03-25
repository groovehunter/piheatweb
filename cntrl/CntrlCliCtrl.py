
from cntrl.models import *
from django.utils import timezone


class CntrlCliCtrl:

  def setup(self):
    self.now = timezone.now()

  def initiate_control_event(self):
    ce = ControlEvent(dtime=self.now)
    ce.save()
