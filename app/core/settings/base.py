# core/settings/base.py
from pathlib import Path

from core.functions import get_env_variable


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = get_env_variable("DJANGO_SECRET_KEY")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "sso.apps.SsoConfig",
    "demo.apps.DemoConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": get_env_variable("DJANGO_DB_ENGINE"),
        "NAME": get_env_variable("DJANGO_DB_NAME"),
        "USER": get_env_variable("DJANGO_DB_USER"),
        "PASSWORD": get_env_variable("DJANGO_DB_PASSWORD"),
        "HOST": get_env_variable("DJANGO_DB_HOST"),
        "PORT": get_env_variable("DJANGO_DB_PORT"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "es-cl"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_L10N = False
USE_TZ = True

DATETIME_FORMAT = "d/m/Y H:i:s"
DATE_FORMAT = "d/m/Y"

STATIC_URL = "static/"
STATIC_ROOT = "/static"
STATICFILES_DIRS = ("staticfiles",)

MEDIA_ROOT = get_env_variable("DJANGO_MEDIA_ROOT", "/media")
MEDIA_URL = "media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = get_env_variable("DJANGO_EMAIL_BACKEND")
EMAIL_HOST = get_env_variable("DJANGO_EMAIL_HOST")
EMAIL_PORT = get_env_variable("DJANGO_EMAIL_PORT")
EMAIL_USE_TLS = get_env_variable("DJANGO_EMAIL_USE_TLS")
EMAIL_HOST_USER = get_env_variable("DJANGO_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = get_env_variable("DJANGO_EMAIL_HOST_PASSWORD")

SERVER_EMAIL = get_env_variable("DJANGO_SERVER_EMAIL")

BASE_URL = get_env_variable("DJANGO_BASE_URL")

# DCC SSO
LOGIN_URL = get_env_variable("DJANGO_LOGIN_URL")
SSO_URL = get_env_variable("DJANGO_SSO_URL")
SSO_APP = get_env_variable("DJANGO_SSO_APP")
SSO_AUTH = get_env_variable("DJANGO_SSO_AUTH")
