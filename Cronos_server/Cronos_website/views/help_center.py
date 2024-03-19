from Cronos_website.views import *


@login_required
def help_center(request) -> HttpResponse:
    """ Render help center page """
    user_pic = UserPic(request.user)
    image_url = user_pic.show_pic()

    context = {
        "image_url": image_url
    }
    return render(request, "help_center.html", context)
