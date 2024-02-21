""" URLs for Cronos_website """

from django.urls import path
from .views import dashboard, home, contact, downloads, help_center, landing_page

app_name = 'Cronos_website'

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('home', home, name='home'),
    path('contact/', contact, name='contact'),
    path('downloads', downloads, name='downloads'),
    path('help_center', help_center, name='help_center'),
    path('dashboard/', dashboard, name='dashboard'),
]
