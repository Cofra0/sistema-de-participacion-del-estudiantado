# core/settings/production.py

from core.settings.base import *


DEBUG = False

ALLOWED_HOSTS = [
    "apps.dcc.uchile.cl",
    "test.dcc.uchile.cl",
    "dev.dcc.uchile.cl",
]

CSRF_TRUSTED_ORIGINS = [
    "https://apps.dcc.uchile.cl",
    "https://test.dcc.uchile.cl",
    "https://dev.dcc.uchile.cl",
]

ADMINS = [
    ("Área de Desarrollo de Software", "desarrollo@dcc.uchile.cl"),
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "include_html": True,
        },
    },
}
