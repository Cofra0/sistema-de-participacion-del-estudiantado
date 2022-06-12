# core/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sso/", include("sso.urls")),
    path("", include("encuestas.urls")),
    path("captcha/", include("captcha.urls")),
]
