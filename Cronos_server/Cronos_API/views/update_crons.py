from Cronos_API.views import *

@api_view(["PUT", "POST"])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def update_cron(request, cron_id):
    cron_instance = get_object_or_404(models.Crons, pk=cron_id)
    cron_serializer = CronsSerializer(
        cron_instance, data=request.data, partial=True
    )

    if not cron_serializer.is_valid():
        return Response(
            cron_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    cron_serializer.save(updated_date=timezone.now())
    create_log(cron_instance.id, "Updated", request.user.id)
    return Response(cron_serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT", "POST"])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def pause_multiple_elements(request):
    data = request.data.get("ids", [])
    for id in data:
        cron_instance = get_object_or_404(models.Crons, id=id)
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
        create_log(cron_instance.id, "Updated", request.user.id)

    return Response(
        {"message": "All crons updated successfully"},
        status=status.HTTP_200_OK
    )


def create_log(cron_id, action, user_id):
    log_data = {
        "log": f"({cron_id}) {action}",
        "create_date": timezone.now(),
        "user": user_id,
        "cron": cron_id,
    }
    log_serializer = LogsSerializer(data=log_data)

    if not log_serializer.is_valid():
        print(log_serializer.errors)
    log_serializer.save()
