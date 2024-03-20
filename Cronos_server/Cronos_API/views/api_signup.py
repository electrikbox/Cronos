from Cronos_API.views import *


@api_view(["POST"])
def signup(request) -> Response:
    """ User Signup """
    user_serializer = UserSerializer(data=request.data)

    if not user_serializer.is_valid():
        return Response(
            user_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    user_instance = user_serializer.save()

    profile_serializer = ProfileSerializer(data=request.data)

    if profile_serializer.is_valid():
        profile_serializer.save(user=user_instance)

    # To be changed to JWT
    token, created = Token.objects.get_or_create(user=user_instance)

    return Response(
        {"message": "Signup successful"},
        headers={"Authorization": f"Token {token.key}"},
    )
