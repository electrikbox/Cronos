from Cronos_website.views import *
from urllib.parse import urlencode


@login_required
def dashboard(request):
    """Render dashboard page"""

    message = request.GET.get('message', None)
    if message:
        messages.success(request, message)

    URL_ERROR_MSG = "URL field is required for this command."
    TOKEN = request.COOKIES.get("user_token")
    HEADER = {
        "Content-Type": "application/json",
        "Authorization": f"Token {TOKEN}",
    }

    if request.method == "POST":
        cron_create_form = CronForm(request.POST)

        if not cron_create_form.is_valid():
            if ("url" in cron_create_form.errors and URL_ERROR_MSG
                in cron_create_form.errors["url"]):
                messages.error(request, URL_ERROR_MSG)
            return redirect("/dashboard")

        command = cron_create_form.cleaned_data['command']
        url = cron_create_form.cleaned_data['url']

        if command == "open":
            command = f"{command} {url}"
        else:
            command = command

        data = {
            "minutes": cron_create_form.cleaned_data["time"].minute,
            "hours": cron_create_form.cleaned_data["time"].hour,
            "day_of_month": cron_create_form.cleaned_data["day_of_month"],
            "months": cron_create_form.cleaned_data["months"],
            "day_of_week": cron_create_form.cleaned_data["day_of_week"],
            "command": command,
            "user": request.user.id,
            "is_paused": False,
            "validated": False,
        }

        response = requests.post(CRON_CREATE_API_URL, headers=HEADER, json=data)

        if response.status_code != 201:
            messages.error(request, "Cron creation failed.")

        return HttpResponseRedirect("/dashboard" + "?create=true")


    else:
        cron_create_form = CronForm()

    crons = requests.get(CRON_LIST_API_URL, headers=HEADER)
    logs = Logs.objects.filter(user=request.user).order_by("create_date").reverse()

    context = {"cron_create_form": cron_create_form, "crons": crons.json(), "logs": logs}
    return render(request, "dashboard.html", context)
