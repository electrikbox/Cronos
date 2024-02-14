from Cronos_API.views import *

@api_view(["POST"])
def login(request) -> Response:
    """ User Login """
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(username=username, password=password)

    if not user:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if not user.is_active:
        return Response(
            status=status.HTTP_401_UNAUTHORIZED,
            data={"message": "Please activate your account first"}
        )

    user.last_login = timezone.now()
    user.save()

    token, created = Token.objects.get_or_create(user=user)
    user_serializer = UserSerializer(instance=user)

    # return Response({"token": token.key, "user": user_serializer.data})
    return Response(
        {"message": "Login successful"},
        headers={'Authorization': f'Token {token.key}'}
    )
