""" Views for Cronos_API """

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import CronsSerializer, LogsSerializer
from Cronos_core import models
from datetime import datetime
from rest_framework import status


# CRONS
# ======================================================

@api_view(['GET'])
def list_crons(request):
    """ List all crons in database """
    crons = models.Crons.objects.all()
    serializer = CronsSerializer(crons, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_cron(request) -> Response:
    """ Add a new cron to database """
    cron_serializer = CronsSerializer(data=request.data)

    if cron_serializer.is_valid():
        cron_instance = cron_serializer.save()

        log_data = {
            "log": "OK",
            "create_date": datetime.now(),
            "user": request.data.get('user'),
            "cron": cron_instance.id,
        }
        
        log_serializer = LogsSerializer(data=log_data)

        if log_serializer.is_valid():
            log_serializer.save()
            return Response(cron_serializer.data, status=status.HTTP_201_CREATED)
        else:
            cron_instance.delete()
            return Response(log_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(cron_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
