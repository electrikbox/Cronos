""" Views for Cronos_API """
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import (
    TokenAuthentication,
    SessionAuthentication,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status
from Cronos_core import models
from .serializers import (
    CronsSerializer,
    LogsSerializer,
    UserSerializer,
    ProfileSerializer,
)


# CRONS Show all
# =============================================================================


@api_view(["GET"])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def list_crons(request) -> Response:
    """List all user's crons"""
    crons = models.Crons.objects.filter(user=request.user)
    serializer = CronsSerializer(crons, many=True)
    return Response(serializer.data)


# CRONS Show one cron
# =============================================================================


@api_view(["GET"])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def show_cron(request, cron_id) -> Response:
    """Show one user's cron by its id"""
    cron_instance = get_object_or_404(models.Crons, pk=cron_id)
    cron_serializer = CronsSerializer(cron_instance)
    return Response(cron_serializer.data)


# CRONS Create
# =============================================================================


@api_view(["POST"])
@authentication_classes([TokenAuthentication, SessionAuthentication])
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
        "log": "Creation OK",
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


# CRONS Update one cron
# =============================================================================


@api_view(["PUT"])
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
        "log": "Update OK",
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


# CRONS Delete
# =============================================================================


@api_view(["DELETE", "POST"])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def delete_cron(request, cron_id) -> Response:
    """Delete a cron by its id"""
    if request.method == "DELETE" or request.method == "POST":
        cron_instance = get_object_or_404(models.Crons, pk=cron_id)
        cron_instance.delete()
        return Response(
            {"message": "Cron deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
    else:
        return Response(
            {"error": "Method not allowed"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

# USER SIGNUP
# =============================================================================


@api_view(["POST"])
def signup(request) -> Response:
    """User Signup"""
    user_serializer = UserSerializer(data=request.data)

    if not user_serializer.is_valid():
        return Response(
            user_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    user_instance = user_serializer.save()

    profile_serializer = ProfileSerializer(data=request.data)

    if profile_serializer.is_valid():
        profile_serializer.save(user=user_instance)

    token, created = Token.objects.get_or_create(user=user_instance)

    # return Response({"token": token.key, "user": user_serializer.data})
    return Response(
        {"message": "Signup successful"},
        headers={"Authorization": f"Token {token.key}"},
    )


# USER LOGIN
# =============================================================================


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
