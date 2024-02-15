""" Class CronFom """

from django import forms
from Cronos_core.models import Crons
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from Cronos_website.forms.cron_form import CronForm
from Cronos_website.forms.forget_password_forms import ForgetPasswordForm, SetNewPasswordForm
from Cronos_website.forms.login_form import LoginFormCustom
from Cronos_website.forms.signup_form import SignUpForm
from Cronos_website.forms.user_account_forms import UserAccountForm, UserAccountPwdForm
