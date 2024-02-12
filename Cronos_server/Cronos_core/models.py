""" Models for Cronos_API
    - Profiles
    - Logs
    - Crons
"""

import datetime
import secrets
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from Cronos_API import COMMANDS


class Profiles(models.Model):
    """ Class Profiles """
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.SET_NULL)


class Logs(models.Model):
    """ Class Logs """
    log = models.CharField(max_length=64)
    create_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cron = models.ForeignKey('Crons', on_delete=models.CASCADE)


class PasswordTemporaryToken(models.Model):
    """ Class for temporary password reset token  """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    change_pwd_token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()


    def save(self, *args, **kwargs):
        """ Generate a token if not exists & set the expiration date """
        if not self.change_pwd_token:
            self.change_pwd_token = secrets.token_urlsafe(32)

        if not self.expires_at:
            self.expires_at = timezone.now() + datetime.timedelta(hours=1) # modif ici le délai
        super().save(*args, **kwargs)


    def is_valid(self):
        """ Check if token is valid  """
        return timezone.now() <= self.expires_at


class Crons(models.Model):
    """ Class Crons """
    minutes = models.CharField(max_length=64)
    hours = models.CharField(max_length=64)
    day_of_month = models.CharField(max_length=64)
    months = models.CharField(max_length=64)
    day_of_week = models.CharField(max_length=64)
    command = models.CharField(max_length=64)

    create_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    validated = models.BooleanField(default=False)
    is_paused = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def get_minutes_choices(cls):
        """ Minutes choices for cron creation """
        choices = [(str(minutes), str(minutes).zfill(2))
                   for minutes in range(0, 60)]
        choices.append(('*', 'each/any'))
        return choices

    @classmethod
    def get_hours_choices(cls):
        """ Hours choices for cron creation """
        choices = [(str(hours), str(hours).zfill(2)) for hours in range(0, 24)]
        choices.append(('*', 'each/any'))
        return choices

    @classmethod
    def get_day_of_month_choices(cls):
        """ Day of the month choice for cron creation """
        choices = [(str(day), str(day).zfill(2)) for day in range(1, 32)]
        choices.append(('*', "each/any"))
        return choices

    @classmethod
    def get_months_choices(cls):
        """ Months choices for cron creation """
        MONTH_NAME = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        choices = [(str(month[:3].lower()), month) for month in MONTH_NAME]
        choices.append(('*', 'each/any'))
        return choices

    @classmethod
    def get_day_of_week_choices(cls):
        """ Day of the week choice for cron creation """
        DAYS_OF_WEEK = [
            'Monday', 'Tuesday', 'Wednesday',
            'Thursday', 'Friday', 'Saturday', 'Sunday'
        ]
        choices = [(str(day[:3].lower()), day) for day in DAYS_OF_WEEK]
        choices.append(('*', "each/any"))
        return choices

    @classmethod
    def get_command_choices(cls):
        """ Command choices for cron creation """
        choices = [(cmd, cmd_form) for cmd, cmd_form in COMMANDS.items()]
        return choices
