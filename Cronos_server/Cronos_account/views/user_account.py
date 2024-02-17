from Cronos_account.views import *


# USER ACCOUNT
# =============================================================================
@login_required
def user_account(request):
    """ Render user account page """
    user = request.user
    profile, created = Profiles.objects.get_or_create(user=user)

    image_url = None

    if request.method == 'POST':
        personal_form = UserAccountForm(request.POST, instance=user)
        password_form = UserAccountPwdForm(request.POST)
        image_form = ProfileImgForm(request.POST, request.FILES)

        if personal_form.is_valid() and personal_form.has_changed():
            personal_form.save()

            profile.first_name = personal_form.cleaned_data['first_name']
            profile.last_name = personal_form.cleaned_data['last_name']
            profile.save()

            return HttpResponseRedirect(reverse('Cronos_account:user_account') + '?updated=true')

        if password_form.is_valid():
            if not user.check_password(password_form.cleaned_data['old_password']):
                messages.error(request, "Invalid old password")
                return HttpResponseRedirect(reverse('Cronos_account:user_account'))

            user.set_password(password_form.cleaned_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)
            return HttpResponseRedirect(reverse('Cronos_account:user_account') + '?updatedPWD=true')

        if image_form.is_valid():
            profile_img = image_form.cleaned_data['profile_img']
            filename, file_extension = os.path.splitext(profile_img.name)

            if file_extension not in ['.jpg', '.jpeg', '.png']:
                messages.error(request, "Invalid image file type")
                return HttpResponseRedirect(reverse('Cronos_account:user_account'))

            filename = f"{user.id}{file_extension.lower()}"
            filepath = os.path.join(settings.MEDIA_ROOT, filename)

            if profile_img.size > 1024 * 1024:
                messages.error(request, "Image file too large ( > 1mb )")
                return HttpResponseRedirect(reverse('Cronos_account:user_account'))

            with open(filepath,'wb') as f:
                for chunk in profile_img.chunks():
                    f.write(chunk)

            image_url = settings.MEDIA_URL + filename

            return HttpResponseRedirect(reverse('Cronos_account:user_account') + '?updatedIMG=true')

    else:
        initial_data = {
            'username': user.username,
            'email': user.email,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
        }
        personal_form = UserAccountForm(instance=user, initial=initial_data)
        password_form = UserAccountPwdForm()
        image_form = ProfileImgForm()

        filename = f"{user.id}.png"
        image_url = settings.MEDIA_URL + filename

    return render(request, 'accounts/user_account.html', {
        'user_account_form': personal_form,
        'user_pwd_form': password_form,
        'profile_img_form': image_form,
        'image_url': image_url,
    })
