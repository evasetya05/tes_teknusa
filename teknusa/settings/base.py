import os
import sys
from pathlib import Path
from django.utils.translation import gettext_lazy as _
import pymysql

pymysql.install_as_MySQLdb()

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent  # Go up one level to reach root directory

sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'extra_apps'))

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-1234567890")

DEBUG = False   # default False, override via dev.py

ALLOWED_HOSTS = []

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = False

SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.sites',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.humanize',
    
    'comment',
    'notice',
    'setting',
    'myzone',
    'home',
    'likeunlike',
    'apps.careers.apps.CareersConfig',
    'apps.contactus.apps.ContactusConfig',
    'about',
    'services',
    'accounts',
    'dashboard.apps.DashboardConfig',

    'leads',
    'lean',
    'ledger',
    'post_media',

    'haystack',
    'mdeditor',
    'ckeditor',
    'ckeditor_uploader',
    'crispy_forms',
    'rest_framework',
    'django_summernote',

    'storages',
    'compressor',

    'blog',
    'portfolio',
    'servermanager',

    'cacheops',
    'django_extensions',
    'django_nose',
    'cookie_consent',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'teknusa.middleware.TimezoneMiddleware',
    'blog.middleware.OnlineMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = "teknusa.urls"
WSGI_APPLICATION = "teknusa.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(PROJECT_ROOT, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'blog.context_processors.seo_processor',
            ]
        },
    }
]

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, "staticfiles")
STATICFILES_DIRS = [os.path.join(PROJECT_ROOT, "static")]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Haystack search configuration
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'teknusa.whoosh_cn_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# CKEditor configuration
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'custom',
        'toolbar_custom': [
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript'],
            ["TextColor", "BGColor", 'RemoveFormat'],
            ['NumberedList', 'BulletedList'],
            ['Link', 'Unlink'],
            ["Smiley", "SpecialChar", 'Blockquote'],
        ],
        'width': 'auto',
        'height': '180',
        'tabSpaces': 4,
        'removePlugins': 'elementspath',
        'resize_enabled': False,
    },
    'comment_ckeditor': {
        'toolbar': 'basic',
        'width': 'auto',
        'height': '120',
        'removePlugins': 'elementspath',
        'resize_enabled': False,
        'toolbar_basic': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList'],
            ['Link', 'Unlink'],
        ],
    },
}

CKEDITOR_UPLOAD_PATH = "uploads/ckeditor/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_ALLOW_NONIMAGE_FILES = True

# Pagination
PAGINATE_BY = 10
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_TIME_FORMAT = '%Y-%m-%d'

SILENCED_SYSTEM_CHECKS = ['mysql.E001']

# Haystack
DJANGO_NOTIFICATIONS_CONFIG = {
    'USE_JSONFIELD': True
}

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LIKES_MODELS = {
    "blog.Article": {
        'serializer': 'article.api.serializers.ArticleSerializer'
    },
    "careers.Job": { },
}

UNICODE_JSON = True

LANGUAGES = [
    ('es', _('Spanish')),
    ('en', _('English')),
    ('de', _('German')),
    ('nl', _('Dutch')),
    ('da', _('Danish')),
    ('hu', _('Hungarian')),
    ('sv', _('Swedish')),
    ('fr', _('French')),
    ('it', _('Italian')),
    ('tr', _('Turkish')),
    ('pt-br', _('Portuguese, Brazilian')),
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other
    'compressor.finders.CompressorFinder',
)

COMPRESS_ENABLED = True
# COMPRESS_OFFLINE = True

COMPRESS_CSS_FILTERS = [
    # creates absolute urls from relative ones
    'compressor.filters.css_default.CssAbsoluteFilter',
    # css minimizer
    'compressor.filters.cssmin.CSSMinFilter'
]
COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter'
]

COOKIE_CONSENT_NAME = "cookie_consent"
COOKIE_CONSENT_MAX_AGE = 60 * 60 * 24 * 365 * 1  # 1 year
COOKIE_CONSENT_LOG_ENABLED = True

FAILED_JOB_THRESHOLD = 20
ACTIVE_JOB_THRESHOLD = 50
ACTIVE_WORKER_THRESHOLD = 5

# AWS Storage config (optional)
# AWS_PUBLIC_MEDIA_LOCATION = os.environ.get('AWS_PUBLIC_MEDIA_LOCATION')
# AWS_STATIC_LOCATION = 'static'
# AWS_PRIVATE_MEDIA_LOCATION = os.environ.get('AWS_PRIVATE_MEDIA_LOCATION')
# AWS_DEFAULT_ACL = None

# Email configuration (will be overridden in production)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# One Signal (optional)
# ONE_SIGNAL_APP_ID = os.environ.get('ONE_SIGNAL_APP_ID')
# ONE_SIGNAL_API_KEY = os.environ.get('ONE_SIGNAL_API_KEY')
