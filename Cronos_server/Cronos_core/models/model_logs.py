from Cronos_core.models import *


class Logs(models.Model):
    """ Class Logs """

    log = models.CharField(max_length=64)
    create_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cron = models.ForeignKey('Crons', on_delete=models.CASCADE)
