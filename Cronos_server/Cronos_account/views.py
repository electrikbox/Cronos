from Cronos_server.mail import activation_mail, forget_password_mail
from Cronos_core.models import ActivationTemporaryToken, PasswordTemporaryToken, Profiles
from Cronos_website.forms import SignUpForm, LoginFormCustom, ForgetPasswordForm, SetNewPasswordForm, UserAccountForm, UserAccountPwdForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.shortcuts import render, redirect, reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required


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

            Token.objects.get_or_create(user=user)

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            activation_token = ActivationTemporaryToken.objects.create(user=user)
            activation_token.save()
            temp_token_key = activation_token.activation_token

            profile = Profiles.objects.create(user=user)
            profile.first_name = first_name
            profile.last_name = last_name
            profile.save()

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
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        temp_token = ActivationTemporaryToken.objects.get(user=user, activation_token=temp_token_key)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ActivationTemporaryToken.DoesNotExist):
        user = None
        temp_token = None

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


# LOGIN USER
# =============================================================================

def login_user(request):
    """ Render login page and authenticate user """
    if request.method == 'POST':
        form = LoginFormCustom(request.POST)

        if form.is_valid() == False:
            return render(request, 'accounts/login.html', {'login_form': form})

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password.")
            return render(request, 'accounts/login.html', {'login_form': form})

        if user.is_active:
            login(request, user)
            token = Token.objects.get(user=request.user).key
            response = HttpResponseRedirect(request.GET.get('next', '/home'))
            response.set_cookie('user_token', token, httponly=True)
            return response

        messages.error(request, "Your account is not active. Please, check your email for activation link.")

    else:
        form = LoginFormCustom()

    return render(request, 'accounts/login.html', {'login_form': form})


# LOGOUT USER
# =============================================================================

def logout_user(request):
    """ Logout user """
    logout(request)
    return redirect('Cronos_account:login')


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
            user.set_password(password_form.cleaned_data['new_password'])
            user.save()
            password_form.save()

            return HttpResponseRedirect(reverse('Cronos_account:user_account') + '?updated=true')
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

# CHANGE PASSWORD
# =============================================================================

def change_password(request):
    """ Render change password page """
    return render(request, 'accounts/change_password.html')


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
        token_temp = PasswordTemporaryToken.objects.get(user=user, change_pwd_token=token_temp_key)

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

        messages.error(request, "The password reset link has expired. Please request a new one")
        return redirect('Cronos_account:forget_password')

    except (TypeError, ValueError, OverflowError, User.DoesNotExist, PasswordTemporaryToken.DoesNotExist):
        messages.error(request, "Invalid password reset link")
        return redirect('Cronos_account:login')
