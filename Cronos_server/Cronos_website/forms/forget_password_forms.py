from Cronos_website.forms import *


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
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirm your password'}),
    )
