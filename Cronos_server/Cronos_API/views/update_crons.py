from Cronos_API.views import *


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_cron(request: WSGIRequest, cron_id) -> Response:
    """ Update a cron by its id """
    cron_instance = get_object_or_404(models.Crons, pk=cron_id)

    # Partial = True / can update only the fields that are provided
    cron_serializer = CronsSerializer(
        cron_instance,
        data=request.data,
        partial=True
    )

    if not cron_serializer.is_valid():
        return Response(
            cron_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    cron_serializer.save(updated_date=timezone.now())

    # Create logs (update)
    create_log(cron_instance.id, "Updated", request.user.id)

    return Response(cron_serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def pause_multiple_elements(request: WSGIRequest) -> Response:
    """ Pause multiple crons by their ids """
    data = request.data.get("ids", [])

    for id in data:
        cron_instance = get_object_or_404(models.Crons, id=id)

        # Partial = True / can update only the fields that are provided
        cron_serializer = CronsSerializer(
            cron_instance,
            data={"is_paused": request.data.get("is_paused")},
            partial=True
        )

        if not cron_serializer.is_valid():
            return Response(
                cron_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        cron_serializer.save(updated_date=timezone.now())

        # Create logs (update)
        create_log(cron_instance.id, "Updated", request.user.id)

    return Response(
        {"message": "All crons updated successfully"},
        status=status.HTTP_200_OK
    )


# Func to create logs
def create_log(cron_id, action, user_id) -> None:
    """ Create logs """
    log_data = {
        "log": f"({cron_id}) {action}",
        "create_date": timezone.now(),
        "user": user_id,
        "cron": cron_id,
    }
    log_serializer = LogsSerializer(data=log_data)

    if not log_serializer.is_valid():
        return Response(
            log_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    log_serializer.save()
