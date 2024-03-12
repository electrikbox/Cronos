from Cronos_API.views import *

@api_view(["GET"])
# @authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def list_logs(request) -> Response:
    """List all user's crons"""
    logs = models.Logs.objects.filter(user=request.user)
    serializer = LogsSerializer(logs, many=True)
    return Response(serializer.data)
