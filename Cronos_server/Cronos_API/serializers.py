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
        fields = [
            "minutes",
            "hours",
            "month"
            "day_of_week",
            "day_of_month",
            "command",
            "user",
            "is_paused",
            "validated"
        ]
        
    def validate_command(self, value: str) -> str:
        if value.split(" ")[0] == "rm":
            raise serializers.ValidationError("command not allowed")
        else:
            return value


# USER
# ====================================================

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'password', 'email']
