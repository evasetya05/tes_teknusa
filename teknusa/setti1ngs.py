import os
import sys
import datetime

from django.utils.translation import gettext_lazy  as _
from dotenv import load_dotenv, find_dotenv
from django_replicated.settings import *
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'extra_apps'))


# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-1234567890")
if not SECRET_KEY:
    raise NameError('SECRET_KEY environment variable is required')
# SECURITY WARNING: don't run with debug turned on in production!

# Application definition
ARTICLE_PAGINATE_BY = 8

BOOK_MOVIE_PAGINATE_BY = 8
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEBUG = True

HAYSTACK_SEARCH_RESULTS_PER_PAGE = 7
INSTALLED_APPS = [
    # Extend the INSTALLED_APPS setting by listing additional applications here
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
    #'notifications',
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
    
    #'xadmin',
    'haystack',
    'mdeditor',
    'ckeditor',
    'crispy_forms',
    'rest_framework',
    'django_summernote',

    'storages',
    #'scheduler',
    'compressor',

    'blog',
    'portfolio',
    'servermanager',

    'cacheops',
    'django_extensions',
    'django_nose',
    'cookie_consent',
    # 'jet_django',
    # Django Elasticsearch integration
    # 'django_elasticsearch_dsl',

    # # Django REST framework Elasticsearch integration (this package)
    # 'django_elasticsearch_dsl_drf',
]
SITE_ID = 1


TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'
COOKIE_CONSENT_LOG_ENABLED = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/'

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

MEDIA_ROOT = os.environ.get('MEDIA_ROOT', './media')
MEDIA_URL = os.environ.get('MEDIA_URL', '/media/')

CKEDITOR_UPLOAD_PATH = "uploads/ckeditor/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_ALLOW_NONIMAGE_FILES = True

# ELASTICSEARCH_DSL = {
#     'default': {
#         'hosts': 'esearch1:9200'
#     },
# }
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'teknusa.whoosh_cn_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
DJANGO_NOTIFICATIONS_CONFIG = {
    'USE_JSONFIELD': True
}
PAGINATE_BY = 10
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_TIME_FORMAT = '%Y-%m-%d'
SILENCED_SYSTEM_CHECKS = ['mysql.E001']

ROOT_URLCONF = "teknusa.urls"
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
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


WSGI_APPLICATION = "teknusa.wsgi.application"

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

'''
untuk development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
'''

import os
import pymysql

pymysql.install_as_MySQLdb()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tes_teknusa',       # ganti dengan nama database kamu
        'USER': 'eva',           # ganti dengan user MySQL
        'PASSWORD': 'abc',   # ganti dengan password MySQL
        'HOST': 'localhost',           # atau IP server MySQL
        'PORT': '3306',                # port default MySQL
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
# JET_PROJECT = 'puneethreddy'
# JET_TOKEN = '508899d1-c612-4ff7-8bde-02b65d9c1b0f'

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

MEDIA_ROOT = os.environ.get('MEDIA_ROOT', './media')

MEDIA_URL = os.environ.get('MEDIA_URL', '/media/')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


PROXY_URL = os.environ.get('PROXY_URL', '')



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
ALERT_HOOK_URL = os.environ.get('ALERT_HOOK_URL')

EMAIL_BACKEND = 'django_amazon_ses.EmailBackend'
AWS_SES_REGION = os.environ.get('AWS_SES_REGION')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
SERVICE_EMAIL_ADDRESS = os.environ.get('SERVICE_EMAIL_ADDRESS')
EMAIL_HOST = os.environ.get('EMAIL_HOST')

# AWS Storage config

AWS_PUBLIC_MEDIA_LOCATION = os.environ.get('AWS_PUBLIC_MEDIA_LOCATION')
AWS_STATIC_LOCATION = 'static'
AWS_PRIVATE_MEDIA_LOCATION = os.environ.get('AWS_PRIVATE_MEDIA_LOCATION')
AWS_DEFAULT_ACL = None

if TESTING:
    OS_TRANSLATION_STRATEGY_NAME = 'testing'
    MIN_UNIQUE_TOP_POST_REACTIONS_COUNT = 1
    MIN_UNIQUE_TOP_POST_COMMENTS_COUNT = 1
    MIN_UNIQUE_TRENDING_POST_REACTIONS_COUNT = 1



    STATIC_URL = '/static/'
    
# ONE SIGNAL
ONE_SIGNAL_APP_ID = os.environ.get('ONE_SIGNAL_APP_ID')
ONE_SIGNAL_API_KEY = os.environ.get('ONE_SIGNAL_API_KEY')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'