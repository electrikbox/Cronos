from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('Cronos_website.urls')),
    path('api/', include('Cronos_API.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    # Autres patterns d'URLs...
]
