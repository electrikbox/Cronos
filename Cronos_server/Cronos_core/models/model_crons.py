from Cronos_core.models import *


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

    separator = ('separator', '-------------')
    each_any = ('*', '*')

    def __str__(self) -> str:
        return str(
            self.minutes + ' ' +
            self.hours + ' ' +
            self.day_of_month + ' ' +
            self.months + ' ' +
            self.day_of_week + ' ' +
            self.command
        )

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
        choices.append(cls.separator)
        choices.append(cls.each_any)
        return choices

    @classmethod
    def get_months_choices(cls):
        """ Months choices for cron creation """
        MONTH_NAME = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        choices = [(str(month[:3].lower()), month) for month in MONTH_NAME]
        choices.append(cls.separator)
        choices.append(cls.each_any)
        return choices

    @classmethod
    def get_day_of_week_choices(cls):
        """ Day of the week choice for cron creation """
        DAYS_OF_WEEK = [
            'Monday', 'Tuesday', 'Wednesday',
            'Thursday', 'Friday', 'Saturday', 'Sunday'
        ]
        choices = [(str(day[:3].lower()), day) for day in DAYS_OF_WEEK]
        choices.append(cls.separator)
        choices.append(cls.each_any)
        return choices

    @classmethod
    def get_command_choices(cls):
        """ Command choices for cron creation """
        choices = [(cmd, cmd_form) for cmd, cmd_form in COMMANDS.items()]
        return choices
