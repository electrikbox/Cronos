""" Mails module for sending emails to users """
from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# ACTIVATION MAIL
# =============================================================================

def activation_mail(email, username, uidb64, token):
    """ Send welcome mail to new user after successful registration """

    # login_url = reverse('Cronos_account:login') + '?success=true'
    # login_url = 'http://localhost:8000/accounts/login/?success=true'

    activation_link = reverse('Cronos_account:activate_account', args=[uidb64, token])
    activation_url = 'http://localhost:8000' + activation_link + '?success=true'

    context = {
		'login_url': activation_url,
  		'username': username,
	}

    email_html_message = render_to_string('mails/activation_mail.html', context)
    email_plain_message = strip_tags(email_html_message)

    send_mail(
        'Welcome to Cronos',
        email_plain_message,
        'Team Cronos',
        [email],
        html_message=email_html_message,
        fail_silently=False,
    )
