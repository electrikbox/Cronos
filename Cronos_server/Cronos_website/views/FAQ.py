from Cronos_website.views import *


@login_required
def FAQ(request) -> HttpResponse:
    """Render FAQ page"""
    return render(request, "FAQ.html")
