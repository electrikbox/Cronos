""" Serializers for Cronos_API """

from rest_framework import serializers
from Cronos_core.models import Logs, Crons
from django.contrib.auth.models import User
from Cronos_API import *


# USER
# =============================================================================


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ["id", "username", "password", "email"]


# LOG
# =============================================================================


class LogsSerializer(serializers.ModelSerializer):
    """Serializer for Logs"""

    class Meta:
        model = Logs
        fields = ["log", "create_date", "user", "cron"]


# CRONS
# =============================================================================


class CronsSerializer(serializers.ModelSerializer):
    """Serializer for Crons"""

    class Meta:
        model = Crons
        fields = [
            "minutes",
            "hours",
            "day_of_month",
            "months",
            "day_of_week",
            "command",
            "user",
            "is_paused",
            "validated",
        ]

    # validate minutes (0 to 59 or  */5 to */55 or *)
    # =========================================================================

    def validate_minutes(self, value: str) -> str:
        if value not in(MINUTES_RANGE + ["*"]):
            raise serializers.ValidationError(MINUTES_ALLOWED_MSG)
        else:
            return value

    # validate hours  (0 to 23 or  */1 to */23 or *)
    # =========================================================================

    def validate_hours(self, value: str) -> str:
        if value not in(HOURS_RANGE + ["*"]):
            raise serializers.ValidationError(HOURS_ALLOWED_MSG)
        else:
            return value


    # validate day of month  (1 to 31 or  */1 to */31 or *)
    # =========================================================================

    def validate_day_of_month(self, value: str) -> str:
        if value not in(DAY_OF_MONTH_RANGE + ["*"]):
            raise serializers.ValidationError(DAY_OF_MONTH_ALLOWED_MSG)

        elif (
            value in (DAY_OF_MONTH_RANGE)
            and (self.initial_data["day_of_week"] != "*")
        ):
            raise serializers.ValidationError(
                DAY_OF_MONTH_ERROR_MSG.format(day_of_month=self.initial_data["day_of_month"]))
        else:
            return value


    # validate months  (1 to 12 or  */1 to */12 or *)
    # =========================================================================

    def validate_months(self, value: str) -> str:
        if value not in (MONTHS_RANGE + ["*"]):
            raise serializers.ValidationError(MONTHS_ALLOWED_MSG)
        else:
            return value


    # validate day of week  (mon, tue, wed, thu, fri, sat, sun or  */1 to */7 or *)
    # =========================================================================

    def validate_day_of_week(self, value: str) -> str:
        if value not in (DAY_OF_WEEK_RANGE + ["*"]):
            raise serializers.ValidationError(DAY_OF_WEEK_ALLOWED_MSG)

        elif (
            value in (DAY_OF_WEEK_RANGE)
            and (self.initial_data["day_of_month"] != "*")
        ):
            raise serializers.ValidationError(
                DAY_OF_WEEK_ERROR_MSG.format(day_of_week=self.initial_data["day_of_week"]))
        else:
            return value


    # validate commands (open, ls)
    # =========================================================================

    def validate_command(self, value: str) -> str:
        if not value.split(" ")[0] in COMMANDS:
            raise serializers.ValidationError(COMMANDS_ALLOWED_MSG)
        else:
            return value
