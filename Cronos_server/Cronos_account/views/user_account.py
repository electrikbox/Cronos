from Cronos_account.views import *


# USER ACCOUNT
# =============================================================================
@login_required
def user_account(request):
    """ Render user account page """
    user = request.user
    profile, created = Profiles.objects.get_or_create(user=user)

    if request.method == 'POST':
        personal_form = UserAccountForm(request.POST, instance=user)
        password_form = UserAccountPwdForm(request.POST)

        if personal_form.is_valid():
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
    else:
        initial_data = {
            'username': user.username,
            'email': user.email,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
        }
        personal_form = UserAccountForm(instance=user, initial=initial_data)
        password_form = UserAccountPwdForm()

    return render(request, 'accounts/user_account.html', {'user_account_form': personal_form, 'user_pwd_form': password_form})
