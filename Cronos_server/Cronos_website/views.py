from django.shortcuts import render
from django.http import HttpResponse
from .form import CronForm


def form(request):
    if request.method == "POST":
        form = CronForm(request.POST)
        if form.is_valid():
            return HttpResponse([form.data[key] for key in ['minutes', 'hours', 'day_of_month', 'months', 'day_of_week', 'command']])
        else:
            return HttpResponse("Error Form")
    else:
        form = CronForm()

    context = {"form": form}

    return render(request, "form.html", context)
