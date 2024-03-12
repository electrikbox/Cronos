from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('Cronos_website.urls')),
    path('api/', include('Cronos_API.urls')),
    path('accounts/', include('Cronos_account.urls')),
    path('admin/', admin.site.urls),
    # Autres patterns d'URLs...
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
