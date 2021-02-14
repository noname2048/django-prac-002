from django.urls import path
from . import views

app_name = "instagram"

urlpatterns = [
    path("", views.root, name="root"),
    path("post/new/", views.post_new, name="post_new"),
]
