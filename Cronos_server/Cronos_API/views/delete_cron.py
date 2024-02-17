from Cronos_API.views import *

@api_view(["DELETE", "POST"])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def delete_cron(request, cron_id) -> Response:
    """Delete a cron by its id"""
    cron_instance = get_object_or_404(models.Crons, pk=cron_id)

    if request.method == "DELETE" or request.method == "POST":

        log_data = {
            "log": f"{cron_id} : Delete OK",
            "create_date": timezone.now(),
            "user": request.user.id,
            "cron": cron_id,
        }

        log_serializer = LogsSerializer(data=log_data)

        if not log_serializer.is_valid():
            print(log_serializer.errors)
            return Response(
                log_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        log_serializer.save()
        cron_instance.delete()
#
        return Response(
            {"message": "Cron deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
    else:
        return Response(
            {"error": "Method not allowed"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )