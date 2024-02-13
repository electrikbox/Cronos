""" URLs for Cronos_website """

from django.urls import path
from .views import dashboard, home, contact, downloads, FAQ, landing_page

app_name = 'Cronos_website'

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('home', home, name='home'),
    path('contact', contact, name='contact'),
    path('downloads', downloads, name='downloads'),
    path('FAQ', FAQ, name='FAQ'),
    path('dashboard/', dashboard, name='dashboard'),
]
