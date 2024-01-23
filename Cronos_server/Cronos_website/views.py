""" Views """
from django.shortcuts import render
from django.http import HttpResponse
from .forms import CronForm


def cron_create_form(request) -> HttpResponse:
    """Render cron_create_form page"""
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
        if cron_create_form.is_valid():
            return HttpResponse(
                " ".join([(cron_create_form.data[key]) for key in fields])
            )
        else:
            return HttpResponse("Error Form")
    else:
        cron_create_form = CronForm()

    context = {"cron_create_form": cron_create_form}

    return render(request, "cron_create_form.html", context)
