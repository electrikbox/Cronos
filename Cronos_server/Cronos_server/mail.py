""" Mails module for sending emails to users """
from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# WELCOME MAIL
# =============================================================================

def welcome_mail(email):
    """ Send welcome mail to new user after successful registration """
    
    # login_url = reverse('accounts:login') + '?success=true'

    login_url = 'http://localhost:8000/accounts/login/?success=true'

    context = {
		'login_url': login_url,
	}

    email_html_message = render_to_string('mails/welcome_mail.html', context)
    email_plain_message = strip_tags(email_html_message)

    send_mail(
        'Welcome to Cronos',
        email_plain_message,
        'Team Cronos',
        [email],
        html_message=email_html_message,
        fail_silently=False,
    )
