from django import forms
from Cronos_core.models import Crons


class CronForm(forms.ModelForm):
    """Crons form class"""
    minutes = forms.ChoiceField(choices=Crons.get_minutes_choices())
    hours = forms.ChoiceField(choices=Crons.get_hours_choices())
    day_of_month = forms.ChoiceField(choices=Crons.get_day_of_month_choices())
    months = forms.ChoiceField(choices=Crons.get_months_choices())
    day_of_week = forms.ChoiceField(choices=Crons.get_day_of_week_choices())
    command = forms.ChoiceField(choices=Crons.get_command_choices())

    class Meta:
        model = Crons
        fields = ['minutes', 'hours', 'day_of_month',
                  'months', 'day_of_week', 'command']
