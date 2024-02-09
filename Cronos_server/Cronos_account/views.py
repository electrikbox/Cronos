from Cronos_server.mail import activation_mail
from Cronos_website.forms import SignUpForm
from Cronos_core.models import Profiles
from Cronos_website.forms import LoginFormCustom
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.shortcuts import render, redirect, reverse
from rest_framework.authtoken.models import Token



# SIGNUP USER
# =============================================================================

def signup_user(request):
    """ Render signup page and create new user """
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                is_active=False
            )
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token, _ = Token.objects.get_or_create(user=user)

            profile = Profiles.objects.create(user=user)
            profile.first_name = first_name
            profile.last_name = last_name
            profile.save()

            activation_mail(email, username, uidb64, token)

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

def activate_account(request, uidb64, token_key):
    """ Activate account after user clicks on activation link """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        token = Token.objects.get(key=token_key)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, Token.DoesNotExist):
        user = None
        token = None

    if user and token and token.user == user:
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse('Cronos_account:login') + '?success=true')
    else:
        return render(request, 'activation_error.html')


# LOGIN USER
# =============================================================================

def login_user(request):
    if request.method == 'POST':
        form = LoginFormCustom(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(request.GET.get('next', '/'))
                else:
                    messages.error(request, "Your account is not active. Please, check your email for activation link.")
                    return render(request, 'accounts/login.html', {'login_form': form})
            else:
                messages.error(request, "Invalid username or password.")
                return render(request, 'accounts/login.html', {'login_form': form})
        else:
            return render(request, 'accounts/login.html', {'login_form': form})
    else:
        form = LoginFormCustom()

    return render(request, 'accounts/login.html', {'login_form': form})


# LOGOUT USER
# =============================================================================

def logout_user(request):
    logout(request)
    return redirect('Cronos_account:login')


# ACCOUNT
# =============================================================================

def account(request):
    """ Render account page """
    return render(request, 'accounts/account.html')


# CHANGE PASSWORD
# =============================================================================

def change_password(request):
    """ Render change password page """
    return render(request, 'accounts/change_password.html')


# FORGET PASSWORD
# =============================================================================

def forget_password(request):
    """ Render forget password page """
    return render(request, 'accounts/forget_password.html')
