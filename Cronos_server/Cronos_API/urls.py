""" URLs for Cronos_API """

from django.urls import path
from .views import list_crons, add_cron, show_cron, update_cron, delete_cron, login, signup, list_logs


app_name = 'Cronos_API'

urlpatterns = [
    path('crons/', list_crons, name='crons'),
    path('crons/create/', add_cron, name='add_cron'),
    path('crons/<cron_id>/', show_cron, name='show_cron'),
    path('crons/<cron_id>/update/', update_cron, name='update_cron'),
    path('crons/<cron_id>/delete/', delete_cron, name='delete_cron'),
    path('logs/', list_logs, name='logs'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
]
