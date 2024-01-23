""" Class CronFom """
from django import forms
from Cronos_core.models import Crons


class CronForm(forms.ModelForm):
    """ Crons form class """
    minutes = forms.ChoiceField(
        choices=Crons.get_minutes_choices(),
        label='Minutes',
        initial=00
    )
    hours = forms.ChoiceField(
        choices=Crons.get_hours_choices(), 
        label='Hours', 
        initial=10
    )
    day_of_month = forms.ChoiceField(
        choices=Crons.get_day_of_month_choices(), 
        label="Month's day", 
        initial='*'
    )
    months = forms.ChoiceField(
        choices=Crons.get_months_choices(), 
        label='Month', 
        initial='*'
    )
    day_of_week = forms.ChoiceField(
        choices=Crons.get_day_of_week_choices(),
        label="Week's day",
        initial='*'
    )
    command = forms.ChoiceField(
        choices=Crons.get_command_choices(),
        label='Command',
        initial='ls'
    )

    class Meta:
        model = Crons
        fields = ['minutes', 'hours', 'day_of_month',
                  'months', 'day_of_week', 'command']
