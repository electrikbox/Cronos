from django.shortcuts import render
from django.http import HttpResponse
from .form import CronForm


def form(request):
    if request.method == "POST":
        form = CronForm(request.POST)
        return HttpResponse(form.data['minutes'])
    else:
        form = CronForm()
    
    context = {"form": form}

    return render(request, "form.html", context)