from .base import *
import os

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "tes_teknusa",
        "USER": "eva",
        "PASSWORD": "abc",
        "HOST": "localhost",
        "PORT": "3306",
        "OPTIONS": {"charset": "utf8mb4"},
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Disable WhiteNoise compression in dev
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
