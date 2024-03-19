from Cronos_website.views import *


def landing_page(request) -> HttpResponse:
    """ Render landing page """

    # Redirect user to homepage if already logged in
    if request.user.is_authenticated:
        return redirect('Cronos_website:home')

    return render(request, "landing-page.html")
