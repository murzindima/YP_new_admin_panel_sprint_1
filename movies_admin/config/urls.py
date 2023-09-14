from django.contrib import admin
from django.urls import path, include

from config.components.debug import DEBUG

urlpatterns = [
    path("admin/", admin.site.urls),
]

if DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
