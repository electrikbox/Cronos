from Cronos_website.views import *


@login_required
def home(request) -> HttpResponse:
    """Render home page"""
    crons_count = Crons.objects.filter(user=request.user).count()

    user_pic = UserPic(request.user)
    image_url = user_pic.show_pic()

    context = {
        "image_url": image_url,
        "crons_count": crons_count,
    }

    return render(request, "home.html", context)
