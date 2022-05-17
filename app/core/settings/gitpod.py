# core/settings/gitpod.py

from core.settings.base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]", "GITPOD_HOST"]

CSRF_TRUSTED_ORIGINS = ["GITPOD_URL"]
