from django.shortcuts import render, redirect
from .form import CronForm


def form(request):
    if request.method == "POST":
        form = CronForm(request.POST)

        if form.is_valid():
            print(f"form is valid")
            return redirect("/cronform/")
    else:
        form = CronForm()

    return render(request, "base.html", {"title": "michel"})