""" Mails module for sending emails to users """

from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# ACTIVATION MAIL
# =============================================================================

def activation_mail(email, username, uidb64, temp_token_key):
    """ Send welcome mail to new user after successful registration """

    # login_url = reverse('Cronos_account:login') + '?success=true'
    # login_url = 'http://localhost:8000/accounts/login/?success=true'

    # Change temp token to JWT
    activation_link = reverse('Cronos_account:activate_account', args=[uidb64, temp_token_key])
    activation_url = 'http://localhost:8000' + activation_link + '?activate=true'

    context = {
		'login_url': activation_url,
  		'username': username,
	}

    email_html_message = render_to_string('mails/activation_mail.html', context)
    email_plain_message = strip_tags(email_html_message) # Remove HTML tags

    # Mail content
    send_mail(
        'Welcome to Cronos', # Subject
        email_plain_message, # Body message
        'Team Cronos', # From ?
        [email], # email user
        html_message=email_html_message,
        fail_silently=False,
    )


# FORGET PASSWORD MAIL
# =============================================================================
def forget_password_mail(email, username, uidb64, token_temp_key):
    """ Send forget password mail to user """

    forget_password_link = reverse('Cronos_account:reset_password', args=[uidb64, token_temp_key])
    forget_password_url = 'http://localhost:8000' + forget_password_link

    context = {
		'forget_password_url': forget_password_url,
        'username': username,
	}

    email_html_message = render_to_string('mails/forget_password_mail.html', context)
    email_plain_message = strip_tags(email_html_message)

    # Mail content
    send_mail(
        'Reset your password',
        email_plain_message,
        'Team Cronos',
        [email],
        html_message=email_html_message,
        fail_silently=False,
    )
