from django import forms
from Cronos_core.models import Crons

class CronForm(forms.ModelForm):
    minutes = forms.ChoiceField(choices=Crons.get_minutes_choices())

    class Meta:
        model = Crons
        fields = ['minutes']
