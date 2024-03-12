from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

def create_jwt_token(user: User):
    refresh: RefreshToken = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def get_access_token(user: User):
    access_token = create_jwt_token(user)['access']
    return access_token

def renew_access_token(user: User):
    refresh_token = create_jwt_token(user)['refresh']
    refresh = RefreshToken(refresh_token)
    access_token = str(refresh.access_token)
    return access_token

# Utilisation :
# user = User.objects.get(username='exemple_user')
# access_token = get_access_token(user)
# Si access_token est expiré, renouveler automatiquement :
# access_token = renew_access_token(user)
