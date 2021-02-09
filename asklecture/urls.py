from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
import debug_toolbar
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
]

if settings.DEBUG:

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
        path("", TemplateView.as_view(template_name="root.html"), name="root"),
    ]

    urlpatterns += static(settings.MEDIA_URL, documments_root=settings.MEDIA_ROOT)
