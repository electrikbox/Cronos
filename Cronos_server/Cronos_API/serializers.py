from rest_framework import serializers
from Cronos_core.models import Crons


class CronsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crons
        fields = ['cron', 'is_paused']
