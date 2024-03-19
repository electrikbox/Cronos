from Cronos_website.views import *


@login_required
def downloads(request) -> HttpResponse:
    """ Render downloads page """
    user_pic = UserPic(request.user)
    image_url = user_pic.show_pic()

    context = {
        "image_url": image_url
    }

    return render(request, "downloads.html", context)
