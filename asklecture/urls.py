from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
import debug_toolbar
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("admin/", admin.site.urls),
]

if settings.DEBUG:

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
        path("accounts/", include("accounts.urls")),
        path("hi/", include("accounts.urls")),
        path("", login_required(TemplateView.as_view(template_name="root.html")), name="root"),
    ]

    urlpatterns += static(settings.MEDIA_URL, documments_root=settings.MEDIA_ROOT)
