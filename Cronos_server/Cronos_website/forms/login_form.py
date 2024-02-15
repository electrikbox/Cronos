from Cronos_website.forms import *


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
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Enter your password'})
    )

    class Meta:
        model = User
        fields = ('username', 'password')
