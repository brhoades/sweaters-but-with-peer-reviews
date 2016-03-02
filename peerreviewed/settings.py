"""
Django settings for peerreviewed project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Pull sensitive/local information from a local file
from peerreviewed.sensitive import SECRET_KEY, DEBUG, ALLOWED_HOSTS, DATABASES

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

TEMPLATE_DEBUG = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djangular',
    'geoposition',
    'django_gravatar',
    'autofixture',
    'sass_processor',

    # Local
    'browse',
    'new',
    'ajax',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'peerreviewed.urls'

WSGI_APPLICATION = 'peerreviewed.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_DIRS = (
    # os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "browse", "static"),
    os.path.join(BASE_DIR, "new", "static"),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "browse", "templates"),
    os.path.join(BASE_DIR, "new", "templates"),
)

BOWER_DIR = os.path.join(BASE_DIR, "browse", "static", "browse",
                         "bower_components")
SASS_PROCESSOR_INCLUDE_DIRS = (
    os.path.join(BASE_DIR, "browse", "static", "browse", "scss"),
    BOWER_DIR,
    os.path.join(BOWER_DIR, "bourbon", "app", "assets", "stylesheets"),
    os.path.join(BOWER_DIR, "mdi", "scss"),
)

SASS_PRECISION = 8

SASS_OUTPUT_STYLE = 'compact'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'middleware.links.link_processor',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

LOGIN_URL = '/logged_in'
