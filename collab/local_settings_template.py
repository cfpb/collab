import sys

ALLOWED_HOSTS = ''

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEPLOYED = False

AUTHENTICATION = 'model'
# or remote_user for Active Directory integration

if AUTHENTICATION == 'model':
    AUTHENICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
    )
else:
    MIDDLEWARE_BACKENDS = MIDDLEWARE_BACKENDS + (
        'django.contrib.auth.middleware.RemoteUserMiddleware',
    )
    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.RemoteUserBackend',
    )


ADMINS = (
    #('Your Name', 'your email'),
)

MANAGERS = ADMINS

if 'test' in sys.argv or 'testserver' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            # path to collab sqlite3 database file
            'NAME': '',
            'USER': '',      # leave empty
            'PASSWORD': '',  # leave empty
            'HOST': '',      # leave empty
            'PORT': '',      # leave empty
        },
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'collab',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',  # Set to empty string for localhost
            'PORT': '',  # Set to empty string for default
        },
    }

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # make sure paths to end with a forward slash,
    # for example, '~/collab/site_static/',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

TEMPLATE_DIRS = (
    # make sure paths to end with a forward slash,
    # for example, '~/collab/templates/',
    './templates',
)

# mail server settings
EMAIL_HOST = ''
EMAIL_PORT = 25
EMAIL_USE_TLS = False

APACHE_HOST = ''

# wiki location
WIKI_URL_BASE = '/wiki/index.php/'
WIKI_HOME = ''
WIKI_INSTALLED = False

from collab.settings import INSTALLED_APPS
INSTALLED_APPS += (
)

# Prepend theme apps to override core
THEMES = (
)
INSTALLED_APPS = THEMES + INSTALLED_APPS

from collab.settings import CACHES
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Prevent local test site from actually trying to send emails
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

FROM_ADDRESS = 'noreply@noreply.com'
