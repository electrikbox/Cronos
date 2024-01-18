""" Views for Cronos_API """

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .serializers import CronsSerializer, LogsSerializer
from Cronos_core import models
from rest_framework import status
from django.utils import timezone


# CRONS Show all
# =============================================================================

@api_view(['GET'])
def list_crons(request) -> Response:
    """ List all crons in database """
    crons = models.Crons.objects.all()
    serializer = CronsSerializer(crons, many=True)
    return Response(serializer.data)


# CRONS Show one cron
# =============================================================================

@api_view(['GET'])
def show_cron(request, cron_id) -> Response:
    """ Show one cron by its id """
    cron_instance = get_object_or_404(models.Crons, pk=cron_id)
    serializer = CronsSerializer(cron_instance)
    return Response(serializer.data)


# CRONS Create
# =============================================================================

@api_view(['POST'])
def add_cron(request) -> Response:
    """ Add a new cron to database """
    cron_serializer = CronsSerializer(data=request.data)

    if cron_serializer.is_valid():
        cron_instance = cron_serializer.save()

        log_data = {
            "log": "Creation OK",
            "create_date": timezone.now(),
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


# CRONS Update one cron
# =============================================================================

@api_view(['PUT'])
def update_cron(request, cron_id) -> Response:
    """ Update a cron by its id """
    cron_instance = get_object_or_404(models.Crons, pk=cron_id)
    cron_serializer = CronsSerializer(
        cron_instance, data=request.data, partial=True)

    if cron_serializer.is_valid():
        cron_serializer.save(updated_date=timezone.now())

        log_data = {
            "log": "Update OK",
            "create_date": timezone.now(),
            "user": cron_instance.user.id if cron_instance.user else None,
            "cron": cron_instance.id,
        }

        log_serializer = LogsSerializer(data=log_data)

        if log_serializer.is_valid():
            log_serializer.save()
            return Response(cron_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(log_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(cron_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# CRONS Delete
# =============================================================================

@api_view(['DELETE'])
def delete_cron(request, cron_id) -> Response:
    """ Delete a cron by its id """
    cron_instance = get_object_or_404(models.Crons, pk=cron_id)
    cron_instance.delete()
    return Response({"message": "Cron deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
