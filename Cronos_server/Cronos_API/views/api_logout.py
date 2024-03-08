from Cronos_API.views import *

@api_view(["POST"])
def logout(request) -> Response:
    """ User Logout """
    token_key = request.data.get("key")

    try:
        token = Token.objects.get(key=token_key)
    except Token.DoesNotExist:
        return Response(
            {"error": "Token does not exist."},
            status=status.HTTP_404_NOT_FOUND
        )

    # token.delete()

    return Response({"message": "Logout successful"})
