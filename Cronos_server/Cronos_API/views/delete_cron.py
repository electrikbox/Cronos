from Cronos_API.views import *
from asgiref.sync import sync_to_async
# from adrf.decorators import api_view
import asyncio

@api_view(["DELETE", "POST"])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def delete_cron(request, cron_id) -> Response:
    """Delete a cron by its id"""
    cron_instance = get_object_or_404(models.Crons, pk=cron_id)

    if request.method == "DELETE" or request.method == "POST":

        log_data = {
            "log": f"({cron_instance.id}) Removed",
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

        return Response(
            {"message": "Cron deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
    else:
        return Response(
            {"error": "Method not allowed"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


@api_view(["DELETE", "POST"])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def delete_multiple_elements(request):
    if request.method == "DELETE" or request.method == "POST":
        data = request.data
        ids_to_delete = data.get("ids", [])

        for id in ids_to_delete:
            cron = get_object_or_404(models.Crons, id=id)
            log_data = {
                "log": f"({cron.id}) Removed",
                "create_date": timezone.now(),
                "user": request.user.id,
                "cron": cron.id,
            }

            log_serializer = LogsSerializer(data=log_data)

            if not log_serializer.is_valid():
                print(log_serializer.errors)
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

# @api_view(["DELETE", "POST"])
# @authentication_classes([TokenAuthentication, SessionAuthentication])
# @permission_classes([IsAuthenticated])
# async def delete_multiple_elements(request):
#     data = request.data
#     ids_to_delete = data.get("ids", [])
#     print(ids_to_delete)
#     print(data)

#     deletion_tasks = []

#     for id in ids_to_delete:
#         deletion_task = asyncio.create_task(delete_element(id))
#         deletion_tasks.append(deletion_task)

#     await asyncio.wait(deletion_tasks)

#     return Response(status=status.HTTP_204_NO_CONTENT)


# @sync_to_async
# def delete_element(id):
#     cron = get_object_or_404(models.Crons, id=id)
#     print(id, cron.command, cron.user)
#     cron.delete()
