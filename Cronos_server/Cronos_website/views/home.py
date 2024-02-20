from Cronos_website.views import *


@login_required
def home(request) -> HttpResponse:
    """Render home page"""
    user_pic = UserPic(request.user)
    image_url = user_pic.show_pic()

    context = {
        "image_url": image_url
    }

    return render(request, "home.html", context)
