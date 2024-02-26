from Cronos_website.views import *
from django.core.paginator import Paginator


URL_ERROR_MSG = "URL field is required for this command."
SOURCE_ERROR_MSG = "Source field is required for this command."
DEST_ERROR_MSG = "Destination field is required for this command."
COMMAND_COOKIE_NAME = "previous_command"


# Main dashboard view
# ==============================================================================


@login_required
def dashboard(request):
    """Render the dashboard page"""
    message = request.GET.get("message", None)
    if message:
        messages.success(request, message)

    TOKEN = request.COOKIES.get("user_token")
    HEADER = {
        "Content-Type": "application/json",
        "Authorization": f"Token {TOKEN}",
    }

    # Retrieve previous command from cookies
    previous_command = request.COOKIES.get(COMMAND_COOKIE_NAME, "")

    if request.method == "POST":
        return handle_post_request(request, HEADER)
    else:
        return render_dashboard_page(request, HEADER, previous_command)


# Handle the POST request to create a cron job
# ==============================================================================


def handle_post_request(request, header):
    """Handle the POST request to create a cron job"""
    cron_create_form = CronForm(request.POST, request.FILES)

    if cron_create_form.is_valid():
        command = get_command_from_form_data(
            cron_create_form.cleaned_data, request
        )
        # Store the command in cookies
        response = create_cron_job(request, cron_create_form, header)
        response.set_cookie(COMMAND_COOKIE_NAME, command)
        return response
    else:
        return handle_invalid_form(request, cron_create_form)


# Create a new cron job and render the dashboard
# ==============================================================================


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


# Get the command from form data
# ==============================================================================


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


# Get the cron job data
# ==============================================================================


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


# Handle an invalid form submission
# ==============================================================================


def handle_invalid_form(request, cron_create_form):
    """Handle an invalid form submission"""
    errors = cron_create_form.errors
    if "url" in errors:
        messages.error(request, URL_ERROR_MSG)
    elif "destination" in errors:
        messages.error(request, DEST_ERROR_MSG)
    elif len(request.FILES) == 0:
        messages.error(request, SOURCE_ERROR_MSG)

    # Store previous command in cookies
    previous_command = request.POST.get("command", "")
    previous_day = request.POST.get("day_of_month", "")
    previous_month = request.POST.get("months", "")
    previous_day_of_week = request.POST.get("day_of_week", "")

    # set cookies and redirect
    response = redirect("/dashboard")
    response.set_cookie(COMMAND_COOKIE_NAME, previous_command)
    response.set_cookie("previous_day", previous_day)
    response.set_cookie("previous_month", previous_month)
    response.set_cookie("previous_day_of_week", previous_day_of_week)
    return response


# Render the dashboard page
# ==============================================================================


def render_dashboard_page(request, header, previous_command):
    """Render the dashboard page"""
    # Use previous command as initial value for the form
    cron_create_form = CronForm(
        initial={
            "command": previous_command,
            "day_of_month": request.COOKIES.get("previous_day", ""),
            "months": request.COOKIES.get("previous_month", ""),
            "day_of_week": request.COOKIES.get("previous_day_of_week", ""),
        }
    )
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
