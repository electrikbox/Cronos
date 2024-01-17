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
    cron = models.CharField(max_length=64)
    create_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    validated = models.BooleanField(default=False)
    is_paused = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
