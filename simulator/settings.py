"""
Django settings for simulator project.

Generated by 'django-admin startproject' using Django 2.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# PRODUCTION ENVIRONMENT SETUP - Need to remove code below this i.e. ones marked under SECURITY WARNING, if sent to production
# SECRET_KEY = os.environ.get('SECRET_KEY')
# HOST = os.environ.get('HOST')
# DEBUG = os.environ.get('DEBUG_VALUE') == 'True'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', default="badsecret")

HOST = os.environ.get('HOST', default="127.0.0.1")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG_VALUE', default='True') == 'True'

ALLOWED_HOSTS = [
    'museum-tracker-api.herokuapp.com'
]


# Application definition
# For production, may need to re-add 'Channels' below before a push to production but I am not sure 
# as I have attempted readding to my development environment and it causes bootstrap errors
# Originally, Paul had me remove this when we worked together to get an environment working
# If you re-add 'Channels' you may have to re-add psycopg2 library to requirements.txt - 'psycopg2==2.8.6'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_tables2',
    'crispy_forms',
    'bootstrap3',
    'game.apps.GameConfig',
    'user.apps.UserConfig',
    'museum.apps.MuseumConfig',
    'badges',
    'schedule',
    'scheduler',
    'payments.apps.PaymentsConfig',
    'paypal.standard.ipn',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'simulator.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'simulator.wsgi.application'

# Channels
ASGI_APPLICATION = "simulator.routing.application"
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DJANGO_SQL_ENGINE", default="django.db.backends.postgresql"),
        "NAME": os.environ.get("DJANGO_SQL_DATABASE", default="hello_django_dev"),
        "USER": os.environ.get("DJANGO_SQL_USER", "hello_django"),
        "PASSWORD": os.environ.get("DJANGO_SQL_PASSWORD", "hello_django"),
        "HOST": os.environ.get("DJANGO_SQL_HOST", "localhost"),
        "PORT": os.environ.get("DJANGO_SQL_PORT", "5432"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EST'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'statcfiles')

# Paypal Info for Sandbox stuff
# https://overiq.com/django-paypal-integration-with-django-paypal/

PAYPAL_RECEIVER_EMAIL = 'sb-rgj5f3725004@business.example.com' # https://developer.paypal.com/developer/accounts/ - just used a sandbox account under my personal paypal for now (will need to change for production)
PAYPAL_TEST = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN')

django_heroku.settings(locals())
