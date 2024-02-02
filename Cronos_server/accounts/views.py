from django.shortcuts import render, redirect, reverse
from Cronos_website.forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from Cronos_core.models import Profiles
from django.contrib.auth.models import User
from Cronos_website.forms import LoginFormCustom
from rest_framework.authtoken.models import Token


# SIGNUP USER
# =============================================================================

def signup_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            user = User.objects.create_user(username=username, password=password, email=email)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            Token.objects.get_or_create(user=user)

            profile = Profiles.objects.create(user=user)


            profile.first_name = first_name
            profile.last_name = last_name
            profile.save()

            return redirect(reverse('accounts:login') + '?success=true')
        else:
            messages.error(request, "Invalid information. Please, try again")
            return render(request, 'accounts/signup.html', {'signup_form': form})
    else:
        form = SignUpForm()
        return render(request, 'accounts/signup.html', {'signup_form': form})


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
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', '/'))
            else:
                messages.error(request, "Invalid username or password.")
                return HttpResponseRedirect(request.GET.get('next', '/'))
    else:
        form = LoginFormCustom()
        return render(request, 'accounts/login.html', {'login_form': form})

# LOGOUT USER
# =============================================================================

def logout_user(request):
    logout(request)
    return redirect('accounts:login')
