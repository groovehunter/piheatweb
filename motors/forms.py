from django import forms



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

