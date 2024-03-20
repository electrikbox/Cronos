from Cronos_API.views import *


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def show_cron(request, cron_id) -> Response:
    """ Show one user's cron by its id """
    cron_instance = get_object_or_404(models.Crons, pk=cron_id)
    cron_serializer = CronsSerializer(cron_instance)

    return Response(cron_serializer.data)
