""" Views """
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from .forms import CronForm
from Cronos_API import CRON_CREATE_API_URL, CRON_LIST_API_URL
import requests


def landing_page(request) -> HttpResponse:
    """ Render FAQ page """
    return render(request, "landing-page.html")

@login_required
def home(request) -> HttpResponse:
    """ Render home page """
    return render(request, "home.html")

@login_required
def contact(request) -> HttpResponse:
    """ Render contact page """
    return render(request, "contact.html")

@login_required
def downloads(request) -> HttpResponse:
    """ Render downloads page """
    return render(request, "downloads.html")

@login_required
def FAQ(request) -> HttpResponse:
    """ Render FAQ page """
    return render(request, "FAQ.html")

@login_required
def dashboard(request):
    """ Render dashboard page """
    token = request.COOKIES.get('user_token')
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Token {token}"
    }

    if request.method == "POST":
        cron_create_form = CronForm(request.POST)
        print(cron_create_form)

        if not cron_create_form.is_valid():
            messages.error(request, 'Please correct the errors below.')
            return redirect('/dashboard')

        print(cron_create_form.cleaned_data)
        data = {
            "minutes": cron_create_form.cleaned_data["time"].minute,
            "hours": cron_create_form.cleaned_data["time"].hour,
            "day_of_month": cron_create_form.cleaned_data["day_of_month"],
            "months": cron_create_form.cleaned_data["months"],
            "day_of_week": cron_create_form.cleaned_data["day_of_week"],
            "command": cron_create_form.cleaned_data["command"],
            "user": request.user.id,
            "is_paused": False,
            "validated": False
        }

        response = requests.post(CRON_CREATE_API_URL, headers=header, json=data)
        messages.success(request, 'Cron added successfully.')
        return redirect('/dashboard')

    else:
        cron_create_form = CronForm()

    crons = requests.get(CRON_LIST_API_URL, headers=header)

    context = {"cron_create_form": cron_create_form, "crons": crons.json()}
    return render(request, "dashboard.html", context)

