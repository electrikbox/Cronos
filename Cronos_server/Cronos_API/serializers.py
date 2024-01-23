""" Serializers for Cronos_API """

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from Cronos_core.models import Logs, Crons, Profiles
from django.contrib.auth.models import User
from Cronos_API import *


# USERS
# =============================================================================


class UserSerializer(serializers.ModelSerializer):
    """ Serializer for Users """
    email = serializers.EmailField(
        validators = [
            UniqueValidator(
                queryset=User.objects.all(),
                message="This email already exists."
            )
        ]
    )
    class Meta(object):
        model = User
        fields = ["id", "username", "password", "email"]

    def create(self, validated_data) -> User:
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# Profiles
# =============================================================================


class ProfileSerializer(serializers.ModelSerializer):
    """ Serializer for Users """
    class Meta(object):
        model = Profiles
        fields = ["id", "first_name", "last_name"]


# LOGS
# =============================================================================


class LogsSerializer(serializers.ModelSerializer):
    """ Serializer for Logs """
    class Meta:
        model = Logs
        fields = ["log", "create_date", "user", "cron"]


# CRONS
# =============================================================================


class CronsSerializer(serializers.ModelSerializer):
    """ Serializer for Crons """
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

    def validate_minutes(self, value: str) -> str:
        """ Validate minutes (0 to 59 or *) """
        if value not in (MINUTES_RANGE + ["*"]):
            raise serializers.ValidationError(MINUTES_ALLOWED_MSG)
        else:
            return value

    def validate_hours(self, value: str) -> str:
        """ Validate hours (0 to 23 or *) """
        if value not in (HOURS_RANGE + ["*"]):
            raise serializers.ValidationError(HOURS_ALLOWED_MSG)
        else:
            return value

    def validate_day_of_month(self, value: str) -> str:
        """ Validate day of month (1 to 31 or *) """
        if value not in (DAY_OF_MONTH_RANGE + ["*"]):
            raise serializers.ValidationError(DAY_OF_MONTH_ALLOWED_MSG)

        elif (
            value in (DAY_OF_MONTH_RANGE)
            and (self.initial_data["day_of_week"] != "*")
        ):
            raise serializers.ValidationError(
                DAY_OF_MONTH_ERROR_MSG.format(
                    day_of_month=self.initial_data["day_of_month"]))
        else:
            return value

    def validate_months(self, value: str) -> str:
        """ Validate months (1 to 12 or *) """
        if value not in (MONTHS_RANGE + ["*"]):
            raise serializers.ValidationError(MONTHS_ALLOWED_MSG)
        else:
            return value

    def validate_day_of_week(self, value: str) -> str:
        """ Validate day of week (mon, tue, wed, thu, fri, sat, sun or *) """
        if value not in (DAY_OF_WEEK_RANGE + ["*"]):
            raise serializers.ValidationError(DAY_OF_WEEK_ALLOWED_MSG)

        elif (
            value in (DAY_OF_WEEK_RANGE)
            and (self.initial_data["day_of_month"] != "*")
        ):
            raise serializers.ValidationError(
                DAY_OF_WEEK_ERROR_MSG.format(
                    day_of_week=self.initial_data["day_of_week"]))
        else:
            return value

    def validate_command(self, value: str) -> str:
        """ Validate commands """
        if not value.split(" ")[0] in COMMANDS:
            raise serializers.ValidationError(COMMANDS_ALLOWED_MSG)
        else:
            return value
