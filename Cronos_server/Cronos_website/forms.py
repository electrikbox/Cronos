""" Class CronFom """
from django import forms
from Cronos_core.models import Crons
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# CLASS CRON FORM
# =============================================================================

class CronForm(forms.ModelForm):
    """ Crons form class """
    minutes = forms.ChoiceField(
        choices=Crons.get_minutes_choices(),
        label='Minutes',
        initial=00
    )
    hours = forms.ChoiceField(
        choices=Crons.get_hours_choices(),
        label='Hours',
        initial=10
    )
    day_of_month = forms.ChoiceField(
        choices=Crons.get_day_of_month_choices(),
        label="Month's day",
        initial='*'
    )
    months = forms.ChoiceField(
        choices=Crons.get_months_choices(),
        label='Month',
        initial='*'
    )
    day_of_week = forms.ChoiceField(
        choices=Crons.get_day_of_week_choices(),
        label="Week's day",
        initial='*'
    )
    command = forms.ChoiceField(
        choices=Crons.get_command_choices(),
        label='Command',
        initial='open_url'
    )
    url = forms.URLField(
        label='Url',
        required=False,
        widget=forms.URLInput(attrs={'placeholder': 'Enter a valid url (ex: https://www.google.com)'}),
    )

    class Meta:
        model = Crons
        fields = ['minutes', 'hours', 'day_of_month',
                  'months', 'day_of_week', 'command']


# CLASS SIGNUP FORM
# =============================================================================

class SignUpForm(UserCreationForm):
    """ Sign up form class """
    username = forms.CharField(
        label="Username",
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}),
    )
    first_name = forms.CharField(
        label="First_name",
        max_length=64,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your firstname'}),
    )
    last_name = forms.CharField(
        label="Last_name",
        max_length=64,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your lastname'}),
    )
    email = forms.EmailField(
        label="Email",
        max_length=50,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter a valid email'}),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Choose a complex password'}),
    )
    password2 = forms.CharField(
        label="Confirm your password",
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirm your password'}),
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')


# CLASS LOGIN FORM
# =============================================================================
class LoginFormCustom(forms.Form):
    """ Login form """
    username = forms.CharField(
        label="username",
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}),
    )
    password = forms.CharField(
        label="password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
    )

    class Meta:
        model = User
        fields = ('username', 'password')


# CLASS FORGET PASSWORD FORM (to set the email to receive the reset link)
# =============================================================================
class ForgetPasswordForm(forms.Form):
    """ Forget password Form """
    email = forms.EmailField(
        label='Your email',
        widget=forms.EmailInput(
            attrs={'placeholder': 'Enter the email associated with your account'}),
    )

    class Meta:
        model = User
        fields = ('email')


# CLASS SET NEW PASSWORD FORM
# =============================================================================
class SetNewPasswordForm(forms.Form):
    """ Set new password form """
    new_password = forms.CharField(
        label="password",
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Choose a new complex password'}),
    )
    new_password_confirm = forms.CharField(
        label="Confirm your password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}),
    )


# USER ACCOUNT PERSONNAL INFO FORM
# =============================================================================
class UserAccountForm(forms.ModelForm):
    """ User account form """
    username = forms.CharField(
        label="Username",
        max_length=15,
    )
    first_name = forms.CharField(
        label="First_name",
        max_length=64,
        required=False,
    )
    last_name = forms.CharField(
        label="Last_name",
        max_length=64,
        required=False,
    )
    email = forms.EmailField(
        label="Email",
        max_length=50,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


# CHANGE PASSWORD FORM in USER ACCOUNT
# =============================================================================
class UserAccountPwdForm(forms.Form):
    """ Change password form in user account """
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)
