from django import forms

hours_list = (
  (1, 1),
  (2, 2),
  (3, 3),
  (6, 6),
  (12, 12),
  (24, 24),
  (48, 48),
)
class GraphAttributesForm(forms.Form):
  sincehours = forms.ChoiceField(label='Since (hours)', choices=hours_list)
  resolution = forms.BooleanField(label='hourly resolution?', required=False)
