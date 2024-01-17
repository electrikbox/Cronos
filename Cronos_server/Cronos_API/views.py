from rest_framework.response import Response
from rest_framework.decorators import api_view
from Cronos_core import models
from .serializers import CronsSerializer


@api_view(['GET'])
def list_crons(request):
    crons = models.Crons.objects.all()
    serializer = CronsSerializer(crons, many=True)
    return Response(serializer.data)
