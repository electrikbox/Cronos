from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from Cronos_website.forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect


def login_user(request):
    if request.method == 'POST':
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
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'login_form': form})


def logout_user(request):
    logout(request)
    return redirect('accounts:login')


def signup_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:login')
        else:
            messages.error(request, "Invalid information. Please, try again.")
            return render(request, 'accounts/signup.html', {'signup_form': form})
    else:
        form = SignUpForm()
        return render(request, 'accounts/signup.html', {'signup_form': form})
