from Cronos_website.forms import *


# CLASS SIGNUP FORM
# =============================================================================

class SignUpForm(UserCreationForm):
    """ Sign up form class """
    username = forms.CharField(
        label="Username",
        max_length=30,
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
