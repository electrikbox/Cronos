from Cronos_API.views import *
from Cronos_API.views.tokens import create_jwt_token

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

    tokens = create_jwt_token(user)
    access_token = tokens['access']
    refresh_token = tokens['refresh']

    response = Response({"message": "Login successful"})
    response.set_cookie('access_token', access_token, httponly=True)
    response.set_cookie('refresh_token', refresh_token, httponly=True)
    return response
