""" Views """
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from .forms import CronForm
from Cronos_API import CRON_CREATE_API_URL
import requests


def home(request) -> HttpResponse:
    """ Render home page """
    return render(request, "home.html")


@login_required
def cron_create_form(request) -> HttpResponse:
    """ Render cron_create_form page """
    fields = [
        "minutes",
        "hours",
        "day_of_month",
        "months",
        "day_of_week",
        "command",
    ]

    if request.method == "POST":
        cron_create_form = CronForm(request.POST)

        if not cron_create_form.is_valid():
            return HttpResponse("Error Form")

        # api request =====================================================

        token = Token.objects.get(user=request.user).key
        header = {                
            "Content-Type": "application/json",
            "Authorization": f"Token {token}"
        }
        data = {field: cron_create_form.data[field] for field in fields}
        data["user"] = request.user.id
        data["is_paused"] = False
        data["validated"] = False
        
        response = requests.post(CRON_CREATE_API_URL, headers=header, json=data)

        if response.status_code == 201:
            context = {"cron_create_form": cron_create_form}
            return render(request, "cron_create_success.html", context)
        else:
            return HttpResponse(response.status_code)
    
        # =================================================================
        
    else:
        cron_create_form = CronForm()

    context = {"cron_create_form": cron_create_form}
    return render(request, "cron_create_form.html", context)
