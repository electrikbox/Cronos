from Cronos_website.forms import *


# CONTACT FORM
# =============================================================================
class ContactForm(forms.Form):
	""" Contact form """
	name = forms.CharField(
		label='Your name',
	)
	email = forms.EmailField(
		label='Your email',
	)
	message = forms.CharField(
            widget=forms.Textarea(attrs={'placeholder': 'Please enter your message here...'}),
  )
