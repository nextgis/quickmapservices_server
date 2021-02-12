"""
Django settings for qms_server project.

Generated by 'django-admin startproject' using Django 1.9.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

from corsheaders.defaults import default_headers

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*p1di8)2ac9=+eb^j=y_6(8a#z%6a(usjo9$83+rb1pn)tl644'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['qms.nextgis.com']
SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'nextgis_common.ngid_auth.auth_backend.NgidBackend',
)

AUTH_USER_MODEL = 'qms_core.NextgisUser'

SESSION_COOKIE_NAME = 'qms_sessionid'
SESSION_COOKIE_AGE = 60 * 60 * 6
CSRF_COOKIE_NAME = 'qms_csrftoken'

LOGOUT_URL = '/logout/'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    'qms_core',
    'qms_site',

    'rest_framework',
    'django_filters',
    'corsheaders',
    # 'captcha',
    'django_crontab',

    'widget_tweaks',
    'django_gravatar',
    'nextgis_common',

    'sslserver'
]

MIDDLEWARE_CLASSES = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'qms_server.wsgi.application'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'qms@nextgis.com'
EMAIL_SUBJECT_PREFIX = '[NextGIS QMS feedback] '

MODIFICATION_API_USERS = [14, 15431]
MODIFICATION_API_BASIC_AUTH = 'Basic cW1zX2FwaV9tb2RpZmljYXRvcjpmOFJqNEdEb3cyUFE='

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    )
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.path.pardir, os.path.pardir, 'static'))
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'frontend/dist'), ]

MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.path.pardir, os.path.pardir, 'media'))

# URLs
ROOT_URLCONF = 'qms_server.urls'

# CORS
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'
CORS_ALLOW_METHODS = (
    'GET',
    'OPTIONS',
)
CORS_ALLOW_HEADERS = default_headers + (
    'range',
    'x-range',
)
CORS_EXPOSE_HEADERS = (
    'content-range',
    'x-content-range',
)

# crontab for update statuses
CRONTAB_LOCK_JOBS = True
CRONJOBS = [
    ('0 0 * * *', 'django.core.management.call_command', ['check_services'], {}, '>> /tmp/update_service_statuces.log'),
]


# try to load local machine settings
try:
    from settings_local import *
except:
    raise

