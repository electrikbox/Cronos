from Cronos_API.views import *


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_cron(request: WSGIRequest, cron_id) -> Response:
    """ Delete a cron by its id """
    cron_instance = get_object_or_404(models.Crons, pk=cron_id)

    if request.method == "DELETE" or request.method == "POST":

        # Create logs (deletion)
        log_data = {
            "log": f"({cron_instance.id}) Removed",
            "create_date": timezone.now(),
            "user": request.user.id,
            "cron": cron_id,
        }

        log_serializer = LogsSerializer(data=log_data)

        if not log_serializer.is_valid():
            return Response(
                log_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        log_serializer.save()
        cron_instance.delete()

        return Response(
            {"message": "Cron deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
    else:
        return Response(
            {"error": "Method not allowed"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_multiple_elements(request: WSGIRequest) -> Response:
    """ Delete multiple crons by their ids """
    if request.method == "DELETE" or request.method == "POST":
        data = request.data
        ids_to_delete = data.get("ids", [])

        # Remove each crons by theirs ids
        for id in ids_to_delete:
            cron = get_object_or_404(models.Crons, id=id)

            # Create logs (deletion)
            log_data = {
                "log": f"({cron.id}) Removed",
                "create_date": timezone.now(),
                "user": request.user.id,
                "cron": cron.id,
            }

            log_serializer = LogsSerializer(data=log_data)

            if not log_serializer.is_valid():
                return Response(
                    log_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            log_serializer.save()
            cron.delete()

        return Response(
            {"message": "Crons deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
    else:
        return Response(
            {"error": "Method not allowed"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
