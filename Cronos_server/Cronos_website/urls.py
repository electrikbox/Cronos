""" URLs for Cronos_website """

from django.urls import path
from .views import cron_create_form, home

app_name = 'Cronos_website'

urlpatterns = [
    path('', home, name='home'),
    path('cronform/', cron_create_form, name='cron_create_form'),
]
