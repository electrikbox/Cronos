from Cronos_website.views import *


def landing_page(request) -> HttpResponse:
    """Render landing page"""
    return render(request, "landing-page.html")
