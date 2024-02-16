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
    url = forms.URLField(
        label='URL',
        required=False,
        widget=forms.URLInput(attrs={'placeholder': 'https://example.com'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        command = cleaned_data.get("command")
        url = cleaned_data.get("url")

        if command == "open" and not url:
            self.add_error("url", "URL field is required for this command.")
        return cleaned_data

    class Meta:
        model = Crons
        fields = ['time', 'day_of_month', 'months', 'day_of_week', 'command', 'url']
