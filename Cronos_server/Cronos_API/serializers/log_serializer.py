from Cronos_API.serializers import *

class LogsSerializer(serializers.ModelSerializer):
    """ Serializer for Logs """
    class Meta:
        model = Logs
        fields = ["log", "create_date", "user", "cron"]
