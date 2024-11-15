
from cntrl.models import *
from django.utils import timezone

import logging
lg = logging.getLogger(__name__)


class CntrlCliCtrl:

  def setup(self):
    self.now = timezone.now()

  def initiate_control_event(self):
    ce = ControlEvent(dtime=self.now)
    lg.debug(ce)
    ce.save()
