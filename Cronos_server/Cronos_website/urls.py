""" URLs for Cronos_website """

from django.urls import path
from .views import cron_create_form, home, contact, downloads, FAQ

app_name = 'Cronos_website'

urlpatterns = [
    path('', home, name='home'),
    path('contact', contact, name='contact'),
    path('downloads', downloads, name='downloads'),
    path('FAQ', FAQ, name='FAQ'),
    path('cronform/', cron_create_form, name='cron_create_form'),
]
