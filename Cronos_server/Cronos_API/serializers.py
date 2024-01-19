""" Serializers for Cronos_API """

from rest_framework import serializers
from Cronos_core.models import Logs, Crons
from django.contrib.auth.models import User


# LOG
# ===================================================

class LogsSerializer(serializers.ModelSerializer):
    """ Serializer for Logs """
    class Meta:
        model = Logs
        fields = ["log", "create_date", "user", "cron"]


# CRONS
# ====================================================

class CronsSerializer(serializers.ModelSerializer):
    """ Serializer for Crons """
    class Meta:
        model = Crons
        fields = ["command", "user", "minutes", "hours", "months", "day_of_week", "day_of_month", "create_date", "updated_date", "is_paused", "validated"]


# USER
# ====================================================

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'password', 'email']
