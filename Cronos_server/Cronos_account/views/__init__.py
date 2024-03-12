""" This module is the package of the views of the Cronos_account app """

import os
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.templatetags.static import static
from Cronos_server.mail import activation_mail, forget_password_mail
from Cronos_core.models import ActivationTemporaryToken, PasswordTemporaryToken, Profiles
from Cronos_website.forms import (
    SignUpForm,
    LoginFormCustom,
    ForgetPasswordForm,
    SetNewPasswordForm,
    UserAccountForm,
    UserAccountPwdForm,
    ProfileImgForm,
)
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.shortcuts import render, redirect, reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required

from Cronos_account.views.forget_password import forget_password, reset_password
from Cronos_account.views.login import login_user, logout_user
from Cronos_account.views.signup import (
    signup_user,
    pending_activation,
    activate_account,
    activation_error
)
from Cronos_account.views.user_account import user_account
