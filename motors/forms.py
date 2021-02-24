from django import forms

from motors.models import Rule

statuslist = (
  ("ON", "on"),
  ("OFF", "off"),
)

amountlist = (
  (200, 200),
  (300, 300),
  (400, 400),
  (500, 500),
  (800, 800),
  (1000, 1000),
)

class MVControlForm(forms.Form):
  amount    = forms.ChoiceField(label='Amount',
    choices = amountlist
    )
  direction = forms.ChoiceField(label='Direction',
    choices = (('up', 'Open'), ('dn', 'Close'))
    )


class MotorControlGenericForm(forms.Form):
  status    = forms.ChoiceField(label='Neuer Status',
    choices = statuslist
    )

class RuleEditForm(forms.ModelForm):
  class Meta:
    model = Rule
    fields = ['name', 'descr', 'logic', 'count']
    exclude = ['id']
