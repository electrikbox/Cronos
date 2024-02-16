from Cronos_website.forms import *


# CLASS CRON FORM
# =============================================================================

class CronForm(forms.Form):
    """ Crons form class """

    time = forms.TimeField(
        label='Time',
        widget=forms.TimeInput(attrs={'type': 'time', 'value': '13:30'}),
    )
    day_of_month = forms.ChoiceField(
        choices=Crons.get_day_of_month_choices(),
        label="Day",
        initial='*',
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
        initial='open_url'
    )

    class Meta:
        model = Crons
        fields = ['time', 'day_of_month', 'months', 'day_of_week', 'command']
