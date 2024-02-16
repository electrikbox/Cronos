""" Class CronFom """
from django import forms
from Cronos_core.models import Crons
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import URLValidator


# CLASS CRON FORM
# =============================================================================

class CronForm(forms.Form):
    """ Crons form class """

    time = forms.TimeField(
        label='Time',
        widget=forms.TimeInput(attrs={'type': 'time', 'value': '13:30'}),
    )
    day_of_month = forms.ChoiceField(
        choices=Crons.get_day_of_month_choices(),
        label="Day",
        initial='*',
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
        label='URL',
        required=False,
        widget=forms.URLInput(attrs={'placeholder': 'https://example.com'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        command = cleaned_data.get("command")
        url = cleaned_data.get("url")

        if command == "open" and not url:
            self.add_error("url", "URL field is required for this command.")
        return cleaned_data

    class Meta:
        model = Crons
        fields = ['time', 'day_of_month', 'months', 'day_of_week', 'command', 'url']


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
