from django.db import models
from cntrl.models import ControlEvent, DEFAULT_EVENT
from django.utils.translation import gettext_lazy as _

# default Rule
DEFAULT_RULE = 1
DEFAULT_MOTOR= 1
DEFAULT_TOGGLE_RULE = 2

class PumpStatus(models.TextChoices):
  RUNNING   = 'Running', _('Running')
  Off       = 'Off', _('Off')
  UNDEFINED = 'Undefined', _('undefined')

class ChangeDirection(models.TextChoices):
  OPENING   = 'Opening', _('Opening')
  CLOSING   = 'Closing', _('Closing')
  NO_CHANGE  = 'No change', _('No change')


""" rules script daemon, jede minute zb schedulen;
Die rules durchgehen, beim einsatz einer regel in die history
tabelle des jeweiligen aktors ein foreignkey auf das aktuellste
ReadingEvent setzen,
Beim aktor ist ja auch schon link zu angewandten regel, so ist
insgesammt nun schon sehr gut semantisch ineinanderpassend.

So ist ReadingEvent der master des chronologischen speicherns
beim loopen durch diese events, kann dann der kombi graph von
sensoren und aktoren erzeugt werden.
"""

#class ActionEvent(models.Model):
#  dtime   = models.DateTimeField('datetime of rule check and actions')

class Mode(models.Model):
  name = models.CharField(max_length=32)
  descr= models.CharField(max_length=255)
  active = models.BooleanField(default=False)


class Rule(models.Model):
  """ Regel in der Gesamtlogik des Regelungssystems """
  name = models.CharField(max_length=32, unique=True)
  descr= models.CharField(max_length=255)
  logic= models.CharField(max_length=255)
  #count= models.PositiveIntegerField()
  with_result = models.BooleanField(default=True)
  active = models.BooleanField(default=True)
  def get_absolute_url(self):
    return self.id
  def __str__(self):
    return self.name

class RuleHistory(models.Model):
  """ Angewandte Regel """ # XXX wie gliedert sich dies ein??
  ctrl_event = models.ForeignKey(ControlEvent,
      on_delete=models.CASCADE,
      default = DEFAULT_EVENT)
  rule = models.ForeignKey(Rule, on_delete=models.CASCADE, default=DEFAULT_RULE)
  result = models.CharField(max_length=20, null=True)
  rule_matched = models.BooleanField(null=True)
  def get_absolute_url(self):
    return self.id
  def __str__(self):
    return self.rule.name + ' - ' + self.ctrl_event.dtime.strftime('%H-%M-%S')


# XXX rename to AktorInfo ?
class Motor(models.Model):
  """ Overview of all actors (Motors, Pumps, Valve ctrl """
  name    = models.CharField(max_length=16)
  descr   = models.CharField(max_length=255)
  pin     = models.PositiveIntegerField(null=True)
  ctrl_class = models.CharField(max_length=50, null=True)

  def get_absolute_url(self):
    return self.id
  def __str__(self):
    return self.name


class WarmwaterPumpHistory(models.Model):
  change_status = models.CharField(null=True, max_length=40,
    choices=PumpStatus.choices,
    default=PumpStatus.UNDEFINED,
    )
  change_descr  = models.CharField(max_length=255)
  rule_event = models.ForeignKey(RuleHistory, on_delete=models.CASCADE, default=DEFAULT_TOGGLE_RULE)

class HeatPumpHistory(models.Model):
  change_status = models.CharField(null=True, max_length=40,
    choices=PumpStatus.choices,
    default=PumpStatus.UNDEFINED,
    )
  change_descr  = models.CharField(max_length=255)
  rule_event    = models.ForeignKey(RuleHistory, on_delete=models.CASCADE, default=DEFAULT_TOGGLE_RULE)

class MainValveHistory(models.Model):
  change_amount = models.IntegerField(null=True)
  change_dir    = models.CharField(
    max_length=12,
    choices=ChangeDirection.choices,
    default=ChangeDirection.NO_CHANGE,
  )
  result_openingdegree = models.IntegerField(null=True)
  rule_event    = models.ForeignKey(RuleHistory, on_delete=models.CASCADE, default=DEFAULT_TOGGLE_RULE)
