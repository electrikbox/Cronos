from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Cronos_API import CRON_CREATE_API_URL, CRON_LIST_API_URL, LOGS_LIST_API_URL
from Cronos_website.forms import CronForm
import requests
from Cronos_core.models import Logs

from Cronos_website.views.landing_page import landing_page
from Cronos_website.views.downloads import downloads
from Cronos_website.views.contact import contact
from Cronos_website.views.FAQ import FAQ
from Cronos_website.views.home import home
from Cronos_website.views.dashboard import dashboard