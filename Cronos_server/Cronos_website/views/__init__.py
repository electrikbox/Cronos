from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

from Cronos_API import CRON_CREATE_API_URL, CRON_LIST_API_URL, LOGS_LIST_API_URL
from Cronos_website.forms import CronForm, ContactForm
from Cronos_account.user_pics import UserPic
from Cronos_core.models import Profiles
from Cronos_core.models import Logs

import requests

from Cronos_website.views.landing_page import landing_page
from Cronos_website.views.downloads import downloads
from Cronos_website.views.contact import contact
from Cronos_website.views.FAQ import FAQ
from Cronos_website.views.home import home
from Cronos_website.views.dashboard import dashboard
from Cronos_website.views.contact import contact
