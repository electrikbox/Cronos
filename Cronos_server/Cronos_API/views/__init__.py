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
from ..serializers import (
    CronsSerializer,
    LogsSerializer,
    UserSerializer,
    ProfileSerializer,
)

from Cronos_API.views.api_login import login
from Cronos_API.views.api_signup import signup
from Cronos_API.views.get_all_crons import list_crons
from Cronos_API.views.get_one_cron_by_id import show_cron
from Cronos_API.views.create_cron import add_cron
from Cronos_API.views.update_crons import update_cron
from Cronos_API.views.delete_cron import delete_cron
from Cronos_API.views.api_signup import signup
from Cronos_API.views.get_all_logs import list_logs
