from django.urls import path
from . import views

app_name = "Cronos_account"

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup_user, name='signup'),
    path('account/', views.account, name='account'),
    path('change_password/', views.change_password, name='change_password'),
    path('forget_password/', views.forget_password, name='forget_password'),
    path('signup/pending/', views.pending_activation, name='pending_activation'),
    path('activate/<uidb64>/<token_key>/', views.activate_account, name='activate_account'),
]
