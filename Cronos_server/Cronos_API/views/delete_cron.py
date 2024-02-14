from Cronos_API.views import *

@api_view(["DELETE", "POST"])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def delete_cron(request, cron_id) -> Response:
    """Delete a cron by its id"""
    if request.method == "DELETE" or request.method == "POST":
        cron_instance = get_object_or_404(models.Crons, pk=cron_id)
        cron_instance.delete()
        return Response(
            {"message": "Cron deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
    else:
        return Response(
            {"error": "Method not allowed"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
