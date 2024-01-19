""" Models for Cronos_API
    - Profiles
    - Logs
    - Crons
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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
        choices.extend((f'*/{minutes}', f'every {minutes}')
                       for minutes in range(5, 60, 5))
        choices.append(('*', 'every minutes'))
        return choices

    @classmethod
    def get_hours_choices(cls):
        """ Hours choices for cron creation """
        choices = [(str(hours), str(hours).zfill(2)) for hours in range(0, 24)]
        choices.extend((f'*/{hours}', f'every {hours}')
                       for hours in range(5, 24, 5))
        choices.append(('*', 'every hours'))
        return choices

    @classmethod
    def get_day_of_month_choices(cls):
        """ Day of the month choice for cron creation """
        choices = [(str(day), str(day).zfill(2)) for day in range(1, 32)]
        choices.extend((f'*/{day}', f'every {day}') for day in range(5, 32, 5))
        choices.append(('*', 'every day of month'))
        return choices

    @classmethod
    def get_months_choices(cls):
        """ Months choices for cron creation """
        months_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                        'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        choices = [(str(month), month) for month in months_names]
        choices.extend((f'*/{month}', f'every {month}')
                       for month in months_names)
        choices.append(('*', 'every month'))
        return choices

    @classmethod
    def get_day_of_week_choices(cls):
        """ Day of the week choice for cron creation """
        days_of_week = ['Monday', 'Tuesday', 'Wednesday',
                        'Thursday', 'Friday', 'Saturday', 'Sunday']
        choices = [(day[:3], day[:3].capitalize()) for day in days_of_week]
        choices.extend((f'*/{day[:3]}', f'every {day[:3]}')
                       for day in days_of_week)
        choices.append(('*', 'every day of the week'))
        return choices

    @classmethod
    def get_command_choices(cls):
        """ Command choices for cron creation """
        choices = [
            ('echo "Hello World"', 'echo "Hello World"'),
            ('ls', 'List Files (ls)'),
            ('pwd', 'Print Working Directory (pwd)'),
        ]
        return choices
