# Django settings for CFPB Intranet collab project.

import sys
import os
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Default user model is 'auth.User', override here
AUTH_USER_MODEL = 'core.CollabUser'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
    'django.template.loaders.filesystem.Loader',
)

# Default Template Context Processors
TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.core.context_processors.static",
"django.core.context_processors.tz",
"django.contrib.messages.context_processors.messages")

TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.request',)
TEMPLATE_CONTEXT_PROCESSORS += ('collab.context_processors.collab_context',)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'collab.middleware.CheckForProfile',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'collab.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'collab.wsgi.application'

INSTALLED_APPS = (
    # django apps
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.markup',
    # 3rd party django apps
    'cache_tools',
    'crispy_forms',
    'haystack',
    'elasticstack',
    'mptt',
    'pipeline',
    'reversion',
    'ordered_model',
    'south',
    'widgeter',
    # collab core apps
    'core',
    'core.notifications',
    'core.search',
    'core.stats',
    'core.taggit',
    'core.custom_comments',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

AUTH_PROFILE_MODULE = 'core.Person'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# wiki location
WIKI_URL_BASE = '/wiki/index.php/'
WIKI_HOME = ''  # WIKI_URL_BASE + 'index.php' -- remove this


PROJECT_PATH = os.path.realpath(os.path.dirname(__file__)) + '/../'
FILES_PATH = PROJECT_PATH + 'files/'


PIPELINE_JS = {
    'main': {
        'source_filenames': (
            'js/jquery-1.8.2.min.js',
            'js/jquery-ui-1.8.24.custom.min.js',
            'jquery.dataTables.min.js',
            'jquery.flexslider-min.js',
            'js/jquery-scrollspy.js',
            'js/jquery.tooltip.min.js',
            'js/jquery.form.js',
            'js/global.js',
            'js/notifications.js',
        ),
        'output_filename': 'js/app.js',
    }
}

PIPELINE_CSS = {
    'base': {
        'source_filenames': (
            'css/style.css',
            'css/jquery.dataTables.css',
            'css/jquery-ui-1.8.24.custom.css',
            'css/notifications.css',
        ),
        'output_filename': 'css/app.css',
    },
}

PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.slimit.SlimItCompressor'

PIPELINE_CSS_COMPRESSOR = None

#   Safe settings for haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

VALID_DOMAINS = ['']

PROJECT_URL = 'http://collab.demo'

COLLAB_CONTEXT = {
}

from collab.local_settings import *
from collab.local_apps import *

if 'test' in sys.argv:
    from collab.test_settings import *

if AUTHENTICATION != 'model':
    MIDDLEWARE_CLASSES += (
        'django.contrib.auth.middleware.RemoteUserMiddleware',)

from settings_helper import load_app_middlewares

MIDDLEWARE_CLASSES = load_app_middlewares(MIDDLEWARE_CLASSES)

COMMENTS_APP = 'core.custom_comments'

# If using elasticsearch, override search_analyzer for ngram/edgengram fields.
# Otherwise, searching for "sample" will return any results that start with "sam"
ELASTICSEARCH_INDEX_SETTINGS = {
    'settings': {
        'analysis': {
            'analyzer': {
                'default': {
                    'type': 'custom',
                    'tokenizer': 'standard',
                    'filter': ['lowercase', 'asciifolding']
                    },
                }
            }
        }
    }


ELASTICSEARCH_DEFAULT_NGRAM_SEARCH_ANALYZER = 'default'
