from Cronos_account.views import *
from Cronos_API.views.tokens import create_jwt_token


# LOGIN USER
# =============================================================================

def login_user(request):
    """ Render login page and authenticate user """
    if request.user.is_authenticated:
        return redirect('Cronos_website:home')

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
            # token = Token.objects.get_or_create(user=user)
            tokens = create_jwt_token(user)
            response = HttpResponseRedirect(request.GET.get('next', '/home'))
            response.set_cookie("user_token", tokens, httponly=True)
            return response

        messages.error(
            request, "Your account is not active. Please, check your email for activation link.")

    else:
        form = LoginFormCustom()

    return render(request, 'accounts/login.html', {'login_form': form})


# LOGOUT USER
# =============================================================================

def logout_user(request):
    """ Logout user """
    # token = Token.objects.get(user=request.user)
    # tokens = create_jwt_token(user)
    # token.delete()

    logout(request)

    return redirect('/')
