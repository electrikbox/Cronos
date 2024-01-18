from django import forms
from Cronos_core.models import Crons

class CronForm(forms.ModelForm):
    class Meta:
        model = Crons
        fields = ["cron"]
        minute = forms.IntegerField(min_value=0, max_value=59)
        hour = forms.IntegerField(min_value=0, max_value=23)
        day_of_month = forms.IntegerField(min_value=1, max_value=31)
        month = forms.IntegerField(min_value=1, max_value=12)
        day_of_week = forms.IntegerField(min_value=0, max_value=6)
        command = forms.CharField(max_length=64)
        widgets = {}
