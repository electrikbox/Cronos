from Cronos_API.views import *
import rest_framework


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_crons(request: rest_framework.request.Request) -> Response:
    """ List all user's crons """
    crons = models.Crons.objects.filter(user=request.user)
    serializer = CronsSerializer(crons, many=True)

    return Response(serializer.data)
