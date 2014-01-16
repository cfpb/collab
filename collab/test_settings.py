TEST_RUNNER = 'django_nose.runner.NoseTestSuiteRunner'

NOSE_WITH_COVERAGE = True
NOSE_WITH_PROGRESSIVE = True
NOSE_ARGS = [
    '-s',
    '--with-progressive',
    '--logging-clear-handlers',
]

SOUTH_TESTS_MIGRATE = False

from collab.settings import INSTALLED_APPS
INSTALLED_APPS += (
    'core.taggit.tests',
    'django_nose',
    'django_factory_boy',
)

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'


from collab.settings import CACHES
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

VALID_DOMAINS = ['']
