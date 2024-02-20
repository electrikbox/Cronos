from operator import is_
from Cronos_website.views import *


@login_required
def contact(request) -> HttpResponse:
    """Render contact page"""
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

    else:
        user = request.user
        if user.is_authenticated:
            try:
                profile = Profiles.objects.get(user=user)
                initial_data = {
                    'name': f"{profile.first_name} {profile.last_name}",
                    'email': user.email
                }
                form = ContactForm(initial=initial_data)
            except Profiles.DoesNotExist:
                form = ContactForm()
        else:
            form = ContactForm()

    user_pic = UserPic(request.user)
    image_url = user_pic.show_pic()

    context = {
        "image_url": image_url,
        "contact_form": form
    }
    return render(request, "contact.html", context)
