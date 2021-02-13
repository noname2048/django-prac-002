from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path("", views.accounts_root, name="root"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    # path("email/", views.test_mail, name="mail"),
    path("edit/", views.profile_edit, name="profile_edit"),
    path("password_change/", views.password_change, name="password_change"),
]
