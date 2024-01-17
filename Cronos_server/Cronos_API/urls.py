""" URLs for Cronos_API """

from django.urls import path
from .views import list_crons, add_cron

app_name = 'Cronos_API'

urlpatterns = [
    path('crons/', list_crons, name='crons'),
    path('crons/create/', add_cron, name='add_cron')
]
