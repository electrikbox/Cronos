""" Views """
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from .forms import CronForm
from Cronos_API import CRON_CREATE_API_URL, CRON_LIST_API_URL
import requests


def home(request) -> HttpResponse:
    """ Render home page """
    return render(request, "home.html")

def contact(request) -> HttpResponse:
    """ Render contact page """
    return render(request, "contact.html")

def downloads(request) -> HttpResponse:
    """ Render downloads page """
    return render(request, "downloads.html")

def FAQ(request) -> HttpResponse:
    """ Render FAQ page """
    return render(request, "FAQ.html")

@login_required
def dashboard(request):
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
            messages.error(request, 'Please correct the errors below.')
            return redirect('/dashboard')

        data = {field: cron_create_form.cleaned_data[field] for field in fields}
        data["user"] = request.user.id
        data["is_paused"] = False
        data["validated"] = False

        token = Token.objects.get(user=request.user).key
        header = {
            "Content-Type": "application/json",
            "Authorization": f"Token {token}"
        }
        data = {field: cron_create_form.cleaned_data[field] for field in fields}
        data["user"] = request.user.id
        data["is_paused"] = False
        data["validated"] = False

        response = requests.post(CRON_CREATE_API_URL, headers=header, json=data)

        messages.success(request, 'Cron added successfully.')

        return redirect('/dashboard')

    else:
        cron_create_form = CronForm()

    token = Token.objects.get(user=request.user).key
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Token {token}"
    }
    crons = requests.get(CRON_LIST_API_URL, headers=header)

    context = {"cron_create_form": cron_create_form, "crons": crons.json()}
    return render(request, "dashboard.html", context)
