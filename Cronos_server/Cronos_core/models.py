from django.db import models
from django.contrib.auth.models import User


class Profiles(models.Model):
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.SET_NULL)


class Crons(models.Model):
    cron = models.CharField(max_length=64)
    validated = models.BooleanField()
    is_paused = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    log = models.ForeignKey('Logs', on_delete=models.CASCADE)


class Logs(models.Model):
    log = models.CharField(max_length=64)
    create_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cron = models.ForeignKey('Crons', on_delete=models.CASCADE)
