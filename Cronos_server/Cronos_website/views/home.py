from Cronos_website.views import *


@login_required
def home(request) -> HttpResponse:
    """ Render home page """

    active_crons_count = Crons.objects.filter(user=request.user, validated=True, is_paused=False).count()
    pending_crons_count = Crons.objects.filter(user=request.user, validated=False).count()
    paused_crons_count = Crons.objects.filter(user=request.user, is_paused=True).count()
    crons_count = Crons.objects.filter(user=request.user).count()

    user_pic = UserPic(request.user)
    image_url = user_pic.show_pic()

    context = {
        "image_url": image_url,
        "crons_count": crons_count,
        "active_crons_count": active_crons_count,
        "pending_crons_count": pending_crons_count,
        "paused_crons_count": paused_crons_count,
    }

    return render(request, "home.html", context)
