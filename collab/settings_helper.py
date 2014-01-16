from collab.settings import INSTALLED_APPS
from django.utils.importlib import import_module


def load_app_middlewares(middleware_classes):
    for app in INSTALLED_APPS:
        try:
            mod = import_module('%s.%s' % (app, 'settings'))
            middleware_classes += mod.MIDDLEWARE_CLASSES
        except:
            continue
    return middleware_classes
