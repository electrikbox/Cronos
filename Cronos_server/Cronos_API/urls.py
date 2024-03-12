""" URLs for Cronos_API """

from django.urls import path
from .views import (
    list_crons,
    add_cron,
    show_cron,
    update_cron,
    delete_cron,
    login,
    logout,
    signup,
    list_logs,
    delete_multiple_elements,
    pause_multiple_elements
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'Cronos_API'

urlpatterns = [
    path('crons/', list_crons, name='crons'),
    path('crons/create/', add_cron, name='add_cron'),
    path('crons/<cron_id>/', show_cron, name='show_cron'),
    path('crons/<cron_id>/update/', update_cron, name='update_cron'),
    path('crons/<cron_id>/delete/', delete_cron, name='delete_cron'),
    path('logs/', list_logs, name='logs'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('signup/', signup, name='signup'),
    path('delete-multiple/', delete_multiple_elements, name='delete_multiple_elements'),
    path('pause-multiple/', pause_multiple_elements, name='pause_multiple_elements'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


]
