""" Serializers for Cronos_API """

from rest_framework import serializers
from Cronos_core.models import Logs, Crons


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
        fields = ["cron", "user", "is_paused", "validated"]
