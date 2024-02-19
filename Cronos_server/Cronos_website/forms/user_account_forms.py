from Cronos_website.forms import *


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


# PROFILE IMAGE FORM in USER ACCOUNT
# =============================================================================
class ProfileImgForm(forms.Form):
    """ Form for uploading profile picture """
    profile_img = forms.ImageField(
        help_text="Max size: 2 MB",
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
        ]
    )
