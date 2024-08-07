import os
from typing import Any, Dict

import dj_database_url
import sentry_sdk
from django_log_formatter_asim import ASIMFormatter
from opensearch_dsl.connections import connections
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from conf.env import env
import healthcheck.backends

from .utils import strip_password_data


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.debug

# As app is running behind a host-based router supplied by Heroku or other
# PaaS, we can open ALLOWED_HOSTS
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    "rest_framework",
    'django_celery_beat',
    'company.apps.CompanyConfig',
    'directory_healthcheck',
    'health_check.db',
    'health_check.cache',
    'drf_spectacular',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

WSGI_APPLICATION = 'conf.wsgi.application'


REDIS_URL = env.redis_url


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {'default': dj_database_url.config(default=env.database_url)}

# Caches
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Static files served with Whitenoise and AWS Cloudfront
# http://whitenoise.evans.io/en/stable/django.html#instructions-for-amazon-cloudfront
# http://whitenoise.evans.io/en/stable/django.html#restricting-cloudfront-to-static-files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
if not os.path.exists(STATIC_ROOT):
    os.makedirs(STATIC_ROOT)
STATIC_HOST = env.static_host
STATIC_URL = STATIC_HOST + '/api-static/'
STATICFILES_STORAGE = env.staticfiles_storage

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

for static_dir in STATICFILES_DIRS:
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.secret_key

# Application authorisation
SIGNATURE_SECRET = env.signature_secret

# DRF
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'conf.signature.SignatureCheckPermission',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

FEATURE_OPENAPI_ENABLED = env.feature_openapi_enabled
SPECTACULAR_SETTINGS = {
    'TITLE': 'Companies House Search API',
    'DESCRIPTION': 'Companies House search service - the Department for Business and Trade (DBT)',
    'VERSION': os.environ.get('GIT_TAG', 'dev'),
}

# Logging for development
if DEBUG:
    LOGGING: Dict[str, Any] = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': True,
            },
            'mohawk': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
            'requests': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
            'opensearchpy': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
        }
    }
else:
    # Sentry logging
    LOGGING: Dict[str, Any] = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'asim_formatter': {
                '()': ASIMFormatter,
            },
            'simple': {
                'style': '{',
                'format': '{asctime} {levelname} {message}',
            },
        },
        'handlers': {
            'asim': {
                'class': 'logging.StreamHandler',
                'formatter': 'asim_formatter',
            },
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'loggers': {
            'django': {
                'handlers': ['asim'],
                'level': 'INFO',
                'propagate': False,
            },
            'sentry_sdk': {
                'handlers': ['asim'],
                'level': 'ERROR',
                'propagate': False,
            },
        },
    }

if env.sentry_dsn:
    sentry_sdk.init(
        dsn=env.sentry_dsn,
        environment=env.sentry_environment,
        integrations=[DjangoIntegration(), CeleryIntegration(), RedisIntegration()],
        before_send=strip_password_data,
        enable_tracing=env.sentry_enable_tracing,
        traces_sample_rate=env.sentry_traces_sample_rate,
    )

# Admin proxy
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_DOMAIN = env.session_cookie_domain
SESSION_COOKIE_NAME = 'chsearch_session_id'
SESSION_COOKIE_SECURE = env.session_cookie_secure
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = env.csrf_cookie_secure


GECKO_API_KEY = env.gecko_api_key
# At present geckoboard's api assumes the password will always be X
GECKO_API_PASS = env.gecko_api_pass

# Celery
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_BROKER_POOL_LIMIT = None

# Elasticsearch
OPENSEARCH_COMPANY_INDEX_ALIAS = env.opensearch_company_index_alias
connections.create_connection(**env.opensearch_config)
OPENSEARCH_CHUNK_SIZE = env.opensearch_chunk_size
OPENSEARCH_TIMEOUT_SECONDS = env.opensearch_timeout_seconds
OPENSEARCH_THREAD_COUNT = env.opensearch_thread_count
OPENSEARCH_USE_PARALLEL_BULK = env.opensearch_use_parallel_bulk

# health check
DIRECTORY_HEALTHCHECK_TOKEN = env.health_check_token
DIRECTORY_HEALTHCHECK_BACKENDS = [
    # health_check.db.backends.DatabaseBackend and
    # health_check.cache.CacheBackend are also registered in
    # INSTALLED_APPS's health_check.db and health_check.cache
    healthcheck.backends.ElasticSearchCheckBackend,
]

CH_DOWNLOAD_URL = 'http://download.companieshouse.gov.uk/en_output.html'

# Companies House
COMPANIES_HOUSE_API_KEY = env.companies_house_api_key

APP_ENVIRONMENT = env.app_environment
