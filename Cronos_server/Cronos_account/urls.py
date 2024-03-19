from django.urls import path
from . import views

""" Urls for user account management """

app_name = "Cronos_account"

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup_user, name='signup'),
    path('signup/activation_error/', views.activation_error, name='activation_error'),
    path('signup/pending/', views.pending_activation, name='pending_activation'),
    path('user_account/', views.user_account, name='user_account'),
    path('forget_password/', views.forget_password, name='forget_password'),
    path('forget_password/reset/<uidb64>/<token_temp_key>/', views.reset_password, name='reset_password'),
    path('activate/<uidb64>/<temp_token_key>/', views.activate_account, name='activate_account'),
]
