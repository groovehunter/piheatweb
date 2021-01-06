from django.db import models

# default Rule
DEFAULT_RULE = 1
DEFAULT_MOTOR= 1
DEFAULT_TOGGLE_RULE = 2


class Rule(models.Model):

    name = models.CharField(max_length=32)
    descr= models.CharField(max_length=255)
    logic= models.CharField(max_length=255)
    count= models.PositiveIntegerField()


class RuleHistory(models.Model):

    rule_id = models.ForeignKey(Rule, on_delete=models.CASCADE, default=DEFAULT_RULE)
    name = models.CharField(max_length=32)
    descr= models.CharField(max_length=255)
    logic= models.CharField(max_length=255)
    count= models.PositiveIntegerField()




class Motor(models.Model):

    name    = models.CharField(max_length=16)
    descr   = models.CharField(max_length=255)
    last_toggle = models.CharField(max_length=16)

    def get_absolute_url(self):
      return self.id


class Toggle(models.Model):

    toggle = models.ForeignKey(Motor, on_delete=models.CASCADE, default=DEFAULT_MOTOR)
    dtime   = models.DateTimeField('date published')
    state   = models.BooleanField('Status')
    rule    = models.ForeignKey(Rule, on_delete=models.CASCADE, default=DEFAULT_TOGGLE_RULE)


from django.utils.translation import gettext_lazy as _
class ChangeDirection(models.TextChoices):
  OPENING   = 'Opening', _('Opening')
  CLOSING   = 'Closing', _('Closing')
  NO_CHANGE  = 'No change', _('No change')


#class MainValve(models.Model):
#  opening_degree = models.IntegerField(null=True)

class MainValveHistory(models.Model):
  dtime         = models.DateTimeField('datetime of change')
  change_amount = models.IntegerField(null=True)
  change_dir    = models.CharField(
    max_length=12,
    choices=ChangeDirection.choices,
    default=ChangeDirection.NO_CHANGE,
  )
  result_openingdegree = models.IntegerField(null=True)
  rule    = models.ForeignKey(Rule, on_delete=models.CASCADE, default=DEFAULT_TOGGLE_RULE)
