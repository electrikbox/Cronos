""" URLs for Cronos_API """

from django.urls import path
from.views import form

app_name = 'Cronos_website'

urlpatterns = [
    path('cronform/', form, name='cronform'),
]
