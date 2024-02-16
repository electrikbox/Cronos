from Cronos_account.views import *


# FORGET PASSWORD
# =============================================================================

def forget_password(request):
    """ Render forget password page """
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')

            try:
                user = User.objects.get(email=email)
                username = user.username

                token_temp = PasswordTemporaryToken.objects.create(user=user)
                token_temp.save()
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token_temp_key = token_temp.change_pwd_token

                forget_password_mail(email, username, uidb64, token_temp_key)

                return HttpResponseRedirect(reverse('Cronos_account:forget_password') + '?pending=true')

            except User.DoesNotExist:
                messages.error(request, "User with this email doesn't exist.")
                return render(request, 'accounts/forget_password.html', {'forget_password_form': form})
    else:
        form = ForgetPasswordForm()
        return render(request, 'accounts/forget_password.html', {'forget_password_form': form})


# RESET FORGOTTEN PASSWORD
# =============================================================================
def reset_password(request, uidb64, token_temp_key):
    """ Render reset forgotten password page """
    try:
        uid = (urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        token_temp = PasswordTemporaryToken.objects.get(
            user=user, change_pwd_token=token_temp_key)

        form = SetNewPasswordForm(request.POST)

        if token_temp.is_valid():
            if request.method == 'POST':
                if form.is_valid():
                    user.set_password(form.cleaned_data['new_password'])
                    user.save()

                    token_temp.delete()
                    return HttpResponseRedirect(reverse('Cronos_account:login') + '?reset=true')
            else:
                return render(request, 'accounts/reset_password.html', {'change_pwd_form': form})

        messages.error(
            request, "The password reset link has expired. Please request a new one")
        return redirect('Cronos_account:forget_password')

    except (TypeError, ValueError, OverflowError, User.DoesNotExist, PasswordTemporaryToken.DoesNotExist):
        messages.error(request, "Invalid password reset link")
        return redirect('Cronos_account:login')
