from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup_user, name='signup'),
    path('account/', views.account, name='account'),
    path('change_password/', views.change_password, name='change_password'),
    path('forget_password/', views.forget_password, name='forget_password'),
]
