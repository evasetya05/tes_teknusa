from .base import *
import os

DEBUG = True  # Production should have DEBUG=False

ALLOWED_HOSTS = ["teknusa.com", "www.teknusa.com"]

# Use environment variable for SECRET_KEY in production
SECRET_KEY = os.getenv("SECRET_KEY", "your-production-secret-key-here-change-this")

import pymysql
pymysql.install_as_MySQLdb()

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "teknusas_teknusa",
        "USER": "teknusas_teknusa",
        "PASSWORD": "@Pontianak123",
        "HOST": "localhost",
        "PORT": "3306",
        "OPTIONS": {"charset": "utf8mb4"},
    }
}

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Email configuration for production
EMAIL_BACKEND = "django_amazon_ses.EmailBackend"
AWS_SES_REGION = os.getenv("AWS_SES_REGION")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Service email (optional)
SERVICE_EMAIL_ADDRESS = os.getenv('SERVICE_EMAIL_ADDRESS')

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
