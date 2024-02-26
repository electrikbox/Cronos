from Cronos_API.serializers import *

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
            "id",
        ]

    def validate_time(self, value: str) -> str:
        """ Validate the time field """
        if value.hour not in HOURS_RANGE or value.minute not in MINUTES_RANGE:
            raise serializers.ValidationError(TIME_ALLOWED_MSG)
        return value

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
        if value not in (DAY_OF_WEEK_RANGE + ["*"] + ["'-------------'"]):
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

    def validate_url(self, value):
        """ Validate URL field only if command is not 'open' """
        command = self.initial_data.get("command")
        url = value

        if command != "open":
            return value
        elif not url:
            raise serializers.ValidationError("URL field is required for this command.")

        return value

    def validate_source(self, value):
        """ Validate source field only if command is not 'cp' """
        command = self.initial_data.get("command")
        source = value

        if command != "cp":
            return value
        elif not source:
            raise serializers.ValidationError("Source field is required for this command.")

        return value

    def validate_destination(self, value):
        """ Validate destination field only if command is not 'cp' """
        command = self.initial_data.get("command")
        destination = value

        if command != "cp":
            return value
        elif not destination:
            raise serializers.ValidationError("Destination field is required for this command.")

        return value
