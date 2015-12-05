"""
Django settings for dotaparty project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import secret

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret.DJANGO_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'huey.djhuey',
    'compressor',
    'core',
    'community'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    #'debug_panel.middleware.DebugPanelMiddleware',
)


ROOT_URLCONF = 'dotaparty.urls'

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
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'dotaparty.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

'''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': secret.PS_DB_NAME,
        'USER': secret.PS_DB_USER,
        'PASSWORD': secret.PS_DB_PW,
        'HOST': secret.PS_DB_HOST,
        'PORT': secret.PS_DB_PORT
    }
}'''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders''.CompressorFinder',
)

COMPRESS_ENABLED = os.environ.get('COMPRESS_ENABLED', False)

HUEY = {
    'backend': 'huey.backends.redis_backend',
    'name': 'dotaparty',
    'connection': {'host': 'localhost', 'port': 6379},
    'consumer_options': {'workers': 4, 'periodic_task_interval': 3},
}

SOCIAL_AUTH_STEAM_API_KEY = secret.D2_API_KEY
LOGIN_REDIRECT_URL = '/'
AUTH_USER_MODEL = 'community.User'

SOCIAL_AUTH_STORAGE = 'community.models.CommunityStorage'

AUTHENTICATION_BACKENDS = (
    'social.backends.steam.SteamOpenId',
    'django.contrib.auth.backends.ModelBackend',
)

import logging
from logging.handlers import RotatingFileHandler

logging.getLogger("requests").setLevel(logging.WARNING)

log_format = ('%(threadName)s %(asctime)s %(name)s '
              '%(levelname)s %(message)s')
handler = RotatingFileHandler(
    'tasks.log', maxBytes=1024 * 1024, backupCount=3)
handler.setFormatter(logging.Formatter(log_format))
task_logger = logging.getLogger('pwm_logger')
task_logger.addHandler(handler)
task_logger.setLevel('INFO')



from django.contrib import admin
from community.models import *
admin.site.register(Report)
