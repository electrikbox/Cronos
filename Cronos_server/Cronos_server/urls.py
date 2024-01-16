from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Cronos_API.urls')),
    # Autres patterns d'URLs...
]
