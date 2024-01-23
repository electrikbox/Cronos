""" URLs for Cronos_website """

from django.urls import path
from .views import cron_create_form

app_name = 'Cronos_website'

urlpatterns = [
    path('cronform/', cron_create_form, name='form'),
]
