from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
import debug_toolbar
from django.views.generic import TemplateView
import django_pydenticon
from django_pydenticon.views import image as pydenticon_image

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="root.html"), name="root"),
    path("accounts/", include("accounts.urls")),
    path("identicon/image/<path:data>/", pydenticon_image, name="pydenticon_image"),
]

if settings.DEBUG:

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
