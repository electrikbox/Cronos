from Cronos_website.views import *
from django.core.paginator import Paginator

# Messages d'erreur constants
URL_ERROR_MSG = "URL field is required for this command."
SOURCE_ERROR_MSG = "Source field is required for this command."
DEST_ERROR_MSG = "Destination field is required for this command."


@login_required
def dashboard(request):
    """Render dashboard page"""
    message = request.GET.get("message", None)
    if message:
        messages.success(request, message)

    TOKEN = request.COOKIES.get("user_token")
    HEADER = {
        "Content-Type": "application/json",
        "Authorization": f"Token {TOKEN}",
    }

    if request.method == "POST":
        return handle_post_request(request, HEADER)

    else:
        return render_dashboard_page(request, HEADER)


def handle_post_request(request, header):
    """Handle POST request for creating a cron job"""
    cron_create_form = CronForm(request.POST, request.FILES)

    if cron_create_form.is_valid():
        return create_cron_job(request, cron_create_form, header)
    else:
        return handle_invalid_form(request, cron_create_form)


def create_cron_job(request, cron_create_form, header):
    """Create a new cron job"""
    command = get_command_from_form_data(cron_create_form.cleaned_data, request)
    data = get_cron_job_data(
        cron_create_form.cleaned_data, command, request.user.id
    )

    response = requests.post(CRON_CREATE_API_URL, headers=header, json=data)

    if response.status_code != 201:
        messages.error(request, "Cron creation failed.")

    return HttpResponseRedirect("/dashboard" + "?create=true")


def get_command_from_form_data(form_data, request):
    """Construct the command based on form data"""
    command = form_data["command"]
    if command == "cp":
        source = request.FILES["name"]
        destination = form_data["destination"]
        command = f"{command} {source} {destination}"
    elif command == "open":
        command = f"{command} {form_data['url']}"
    return command


def get_cron_job_data(form_data, command, user_id):
    """Construct the data for creating a cron job"""
    return {
        "minutes": form_data["time"].minute,
        "hours": form_data["time"].hour,
        "day_of_month": form_data["day_of_month"],
        "months": form_data["months"],
        "day_of_week": form_data["day_of_week"],
        "command": command,
        "user": user_id,
        "is_paused": False,
        "validated": False,
    }


def handle_invalid_form(request, cron_create_form):
    """Handle an invalid form submission"""
    if "url" in cron_create_form.errors:
        messages.error(request, URL_ERROR_MSG)
    elif "destination" in cron_create_form.errors:
        messages.error(request, DEST_ERROR_MSG)
    elif len(request.FILES) == 0:
        messages.error(request, SOURCE_ERROR_MSG)
    return redirect("/dashboard")


def render_dashboard_page(request, header):
    """Render the dashboard page"""
    cron_create_form = CronForm()
    crons = requests.get(CRON_LIST_API_URL, headers=header).json()
    paginator = Paginator(crons, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    logs = (
        Logs.objects.filter(user=request.user).order_by("create_date").reverse()
    )
    user_pic = UserPic(request.user)
    image_url = user_pic.show_pic()
    context = {
        "cron_create_form": cron_create_form,
        "crons": crons,
        "logs": logs,
        "image_url": image_url,
        "page_obj": page_obj,
    }
    return render(request, "dashboard.html", context)
