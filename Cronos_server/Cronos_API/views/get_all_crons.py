from Cronos_API.views import *

@api_view(["GET"])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def list_crons(request) -> Response:
    """List all user's crons"""
    crons = models.Crons.objects.filter(user=request.user)
    serializer = CronsSerializer(crons, many=True)
    return Response(serializer.data)
