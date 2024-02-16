from Cronos_website.views import *


@login_required
def contact(request) -> HttpResponse:
    """Render contact page"""
    return render(request, "contact.html")
