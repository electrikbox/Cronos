""" Views """
from django.shortcuts import render
from django.http import HttpResponse
from .form import CronForm


def form(request) -> HttpResponse:
    """ Render Form page """
    fields = [
        'minutes',
        'hours',
        'day_of_month',
        'months',
        'day_of_week',
        'command'
    ]

    if request.method == "POST":
        form = CronForm(request.POST)
        if form.is_valid():
            return HttpResponse(' '.join([(form.data[key]) for key in fields]))
        else:
            return HttpResponse("Error Form")
    else:
        form = CronForm()

    context = {"form": form}

    return render(request, "form.html", context)
