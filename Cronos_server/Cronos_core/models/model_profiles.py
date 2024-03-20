from typing import Any
from Cronos_core.models import *


class Profiles(models.Model):
    """ Class Profiles """

    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        """ String representation of profiles """
        return f"{self.first_name} {self.last_name}"
