from Cronos_website.views import *


@login_required
def home(request) -> HttpResponse:
    """Render home page"""
    return render(request, "home.html")
