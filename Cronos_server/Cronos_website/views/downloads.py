from Cronos_website.views import *


@login_required
def downloads(request) -> HttpResponse:
    """Render downloads page"""
    return render(request, "downloads.html")
