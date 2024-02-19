from Cronos_API.views import *

@api_view(["PUT", "POST"])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def update_cron(request, cron_id) -> Response:
    """Update a cron by its id"""
    cron_instance = get_object_or_404(models.Crons, pk=cron_id)
    cron_serializer = CronsSerializer(
        cron_instance, data=request.data, partial=True
    )

    if not cron_serializer.is_valid():
        return Response(
            cron_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    cron_serializer.save(updated_date=timezone.now())

    log_data = {
        "log": f"({cron_instance.id}) Updated",
        "create_date": timezone.now(),
        "user": cron_instance.user.id if cron_instance.user else None,
        "cron": cron_instance.id,
    }

    log_serializer = LogsSerializer(data=log_data)

    if not log_serializer.is_valid():
        return Response(
            cron_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    log_serializer.save()
    return Response(cron_serializer.data, status=status.HTTP_200_OK)
