from django.urls import path
from .views import list_crons

urlpatterns = [
    path('crons/', list_crons, name='crons'),
]
