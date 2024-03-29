from Cronos_account.views import *


# SIGNUP USER
# =============================================================================

def signup_user(request):
    """ Render signup page and create new user """
    if request.user.is_authenticated:
        return redirect('Cronos_website:home')

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            # To be changed to api request

            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            # Create User
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                is_active=False
            )
            user.save()

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            activation_token = ActivationTemporaryToken.objects.create(
                user=user)
            activation_token.save()

            # To be changed to JWT
            temp_token_key = activation_token.activation_token

            # Create User Profile
            profile = Profiles.objects.create(user=user)
            profile.first_name = first_name
            profile.last_name = last_name
            profile.save()

            # Send activation email
            activation_mail(email, username, uidb64, temp_token_key)

            return redirect('Cronos_account:pending_activation')
        else:
            messages.error(request, "Invalid information. Please, try again")
            return render(request, 'accounts/signup.html', {'signup_form': form})
    else:
        form = SignUpForm()
        return render(request, 'accounts/signup.html', {'signup_form': form})


# PENDING ACTIVATION
# =============================================================================

def pending_activation(request):
    """ Render pending account page """
    return render(request, 'accounts/pending_activation.html')


# ACTIVATE ACCOUNT
# =============================================================================

def activate_account(request, uidb64, temp_token_key):
    """ Activate account after user clicks on activation link """
    try:
        # Security id for url
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        temp_token = ActivationTemporaryToken.objects.get(
            user=user, activation_token=temp_token_key)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ActivationTemporaryToken.DoesNotExist):
        user = None
        temp_token = None

    # Check if user and temp token exists and are valid
    if user and temp_token and temp_token.is_valid():
        user.is_active = True
        user.save()
        temp_token.delete()
        return HttpResponseRedirect(reverse('Cronos_account:login') + '?activate=true')
    else:
        return render(request, 'accounts/activation_error.html')


# ACTIVATION ERROR
# =============================================================================

def activation_error(request):
    """ Render activation error page """
    return render(request, 'accounts/activation_error.html')
