from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model


User = get_user_model()


def create_jwt_token(user: User):
    """ Create JWT tokens for user """
    refresh: RefreshToken = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def get_access_token(user: User):
    """ Get access token for user """
    access_token = create_jwt_token(user)['access']

    return access_token

def renew_access_token(user: User):
    """ Renew access token for user """
    refresh_token = create_jwt_token(user)['refresh']
    refresh = RefreshToken(refresh_token)
    access_token = str(refresh.access_token)

    return access_token
