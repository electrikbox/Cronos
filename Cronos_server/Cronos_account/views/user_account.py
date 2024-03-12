from Cronos_account.views import *
from ..user_pics import UserPic

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

        # PERSONAL INFO FORM
        if personal_form.is_valid() and personal_form.has_changed():
            personal_form.save()

            profile.first_name = personal_form.cleaned_data['first_name']
            profile.last_name = personal_form.cleaned_data['last_name']
            profile.save()

            return HttpResponseRedirect(reverse('Cronos_account:user_account') + '?updated=true')

        # PASSWORD (change) FORM
        if password_form.is_valid():
            if not user.check_password(password_form.cleaned_data['old_password']):
                messages.error(request, "Invalid old password")
                return HttpResponseRedirect(reverse('Cronos_account:user_account'))

            user.set_password(password_form.cleaned_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)
            return HttpResponseRedirect(reverse('Cronos_account:user_account') + '?updatedPWD=true')

        # PROFILE PICTURE FORM
        if image_form.is_valid():
            user_pic = UserPic(user)
            profile_pic = user_pic.upload_pic(
                image_form.cleaned_data['profile_img'])

            return HttpResponseRedirect(reverse('Cronos_account:user_account') + '?updatedIMG=true')
        else:
            for field, errors in image_form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")

            return HttpResponseRedirect(reverse('Cronos_account:user_account'))

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

        user_pic = UserPic(user)
        image_url = user_pic.show_pic()

    return render(request, 'accounts/user_account.html', {
        'user_account_form': personal_form,
        'user_pwd_form': password_form,
        'profile_img_form': image_form,
        'image_url': image_url,
    })
