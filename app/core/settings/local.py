# core/settings/docker.py

from core.settings.base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]

CSRF_TRUSTED_ORIGINS = ["http://localhost:8000"]
