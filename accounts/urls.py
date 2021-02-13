from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.accounts_root, name="root"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    # path("email/", views.test_mail, name="mail"),
]
