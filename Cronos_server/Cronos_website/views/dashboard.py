from Cronos_website.views import *
from django.core.paginator import Paginator
from django.core.handlers.wsgi import WSGIRequest


URL_ERROR_MSG = "URL field is required for this command."
SOURCE_ERROR_MSG = "Source field is required for this command."
SOURCE_SPACE_ERROR_MSG = "Source field can't have spaces."
DEST_ERROR_MSG = "Destination field is required for this command."
DEST_SPACE_ERROR_MSG = "Destination field can't have spaces."
COMMAND_COOKIE_NAME = "previous_command"


# Main dashboard view
# ==============================================================================


@login_required
def dashboard(request: WSGIRequest) -> HttpResponseRedirect | HttpResponse:
    """Render the dashboard page"""
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


# Handle the POST request to create a cron job
# ==============================================================================


def handle_post_request(request: WSGIRequest, header: dict) -> HttpResponseRedirect:
    """Handle the POST request to create a cron job"""
    cron_create_form = CronForm(request.POST, request.FILES)

    if cron_create_form.is_valid():
        command = get_command_from_form_data(
            cron_create_form.cleaned_data,
            request
        )
        # Store the command in cookies
        response = create_cron_job(request, cron_create_form, header)
        response.set_cookie(COMMAND_COOKIE_NAME, command)
        return response
    else:
        return handle_invalid_form(request, cron_create_form)


# Create a new cron job and render the dashboard
# ==============================================================================


def create_cron_job(request: WSGIRequest, cron_create_form: CronForm, header: dict) -> HttpResponseRedirect:
    """Create a new cron job"""
    command = get_command_from_form_data(
        cron_create_form.cleaned_data,
        request
    )
    data = get_cron_job_data(
        cron_create_form.cleaned_data,
        command,
        request.user.id
    )

    response = requests.post(CRON_CREATE_API_URL, headers=header, json=data)

    if response.status_code != 201:
        messages.error(request, "Cron creation failed.")

    return HttpResponseRedirect("/dashboard" + "?create=true")


# Get the command from form data
# ==============================================================================


def get_command_from_form_data(form_data: dict, request: WSGIRequest) -> str:
    """Construct the command based on form data"""
    command = form_data["command"]

    if command == "cp" or command == "ls":
        # source = request.FILES["name"]
        source = form_data["source"]
        destination = form_data["destination"]
        command = f"{command} {source} {destination}"

    elif command == "open":
        command = f"{command} {form_data['url']}"

    return command


# Get the cron job data
# ==============================================================================


def get_cron_job_data(form_data: dict, command: str, user_id: int) -> dict:
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


# Handle an invalid form submission
# ==============================================================================


def handle_invalid_form(request: WSGIRequest, cron_create_form: CronForm) -> HttpResponseRedirect:
    """Handle an invalid form submission"""

    errors = cron_create_form.errors
    if "url" in errors:
        messages.error(request, URL_ERROR_MSG)
    elif "source" in errors:
        if "space" in errors["source"]:
            messages.error(request, SOURCE_SPACE_ERROR_MSG)
        else:
            messages.error(request, SOURCE_ERROR_MSG)
    elif "destination" in errors:
        if "space" in errors["destination"]:
            messages.error(request, DEST_SPACE_ERROR_MSG)
        else:
            messages.error(request, DEST_ERROR_MSG)

    # Store previous command in cookies
    previous_command = request.POST.get("command", "")
    previous_day = request.POST.get("day_of_month", "")
    previous_month = request.POST.get("months", "")
    previous_day_of_week = request.POST.get("day_of_week", "")

    response = redirect("/dashboard")
    response.set_cookie(COMMAND_COOKIE_NAME, previous_command)
    response.set_cookie("previous_day", previous_day)
    response.set_cookie("previous_month", previous_month)
    response.set_cookie("previous_day_of_week", previous_day_of_week)
    return response


# Render the dashboard page
# ==============================================================================


def render_dashboard_page(request: WSGIRequest, header: dict) -> HttpResponse:
    """Render the dashboard page"""

    previous_command = request.COOKIES.get(COMMAND_COOKIE_NAME, "")
    previous_day = request.COOKIES.get("previous_day", "")
    previous_month = request.COOKIES.get("previous_month", "")
    previous_day_of_week = request.COOKIES.get("previous_day_of_week", "")

    if (not previous_command or
        not previous_day or
        not previous_month or
        not previous_day_of_week):
        set_initial = {
            "command": "open_url",
            "day_of_month": '*',
            "months": '*',
            "day_of_week": '*',
        }
    else:
        set_initial = {
            "command": previous_command,
            "day_of_month": previous_day,
            "months": previous_month,
            "day_of_week": previous_day_of_week,
        }

    # Use previous command as initial value for the form
    cron_create_form = CronForm(initial=set_initial)
    crons = requests.get(CRON_LIST_API_URL, headers=header).json()
    paginator = Paginator(crons, 7)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    logs = (
        Logs.objects
        .filter(user=request.user)
        .order_by("create_date").reverse()
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
