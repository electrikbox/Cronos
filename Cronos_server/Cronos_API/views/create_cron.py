from Cronos_API.views import *

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_cron(request) -> Response:
    """Add a new cron to database"""
    cron_serializer = CronsSerializer(data=request.data)

    if not cron_serializer.is_valid():
        return Response(
            cron_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    cron_instance = cron_serializer.save()

    log_data = {
        "log": f"({cron_instance.id}) Created",
        "create_date": timezone.now(),
        "user": request.data.get("user"),
        "cron": cron_instance.id,
    }

    log_serializer = LogsSerializer(data=log_data)

    if not log_serializer.is_valid():
        return Response(
            cron_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    log_serializer.save()
    return Response(cron_serializer.data, status=status.HTTP_201_CREATED)
