from Cronos_website.views import *


def landing_page(request) -> HttpResponse:
    """Render FAQ page"""
    return render(request, "landing-page.html")