import datetime
import factory

from django.conf import settings
from django.contrib.auth import models, get_user_model
from django.contrib.contenttypes import models as ctmodels
from django.db.models import get_model, Model
from django.utils import timezone

__all__ = (
    'UserF',
    'PermissionF',
    'GroupF',
    'ContentTypeF',
)


class GroupF(factory.Factory):
    FACTORY_FOR = models.Group

    @classmethod
    def _setup_next_sequence(cls):
        try:
            return cls._associated_class.objects.values_list(
                'id', flat=True).order_by('-id')[0] + 1
        except IndexError:
            return 0

    name = factory.Sequence(lambda n: "group%s" % n)


class UserF(factory.Factory):
    FACTORY_FOR = get_user_model()

    @classmethod
    def _setup_next_sequence(cls):
        try:
            return cls._associated_class.objects.values_list(
                'id', flat=True).order_by('-id')[0] + 1
        except IndexError:
            return 0

    username = factory.Sequence(lambda n: "username%s" % n)
    first_name = factory.Sequence(lambda n: "first_name%s" % n)
    last_name = factory.Sequence(lambda n: "last_name%s" % n)
    email = factory.Sequence(lambda n: "email%s@example.com" % n)
    password = 'pbkdf2_sha256$10000$ggAKkiHobFL8$xQzwPeHNX1vWr9uNmZ/gKbd17uLGZVM8QNcgmaIEAUs='
    is_staff = False
    is_active = True
    is_superuser = False
    last_login = timezone.now()
    date_joined = timezone.now()


def user_create(cls, **kwargs):
    # figure out the profile's related name and strip profile's kwargs
    profile_model, profile_kwargs = None, {}
    try:
        app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
    except (ValueError, AttributeError):
        pass
    else:
        try:
            profile_model = get_model(app_label, model_name)
        except (ImportError, ImproperlyConfigured):
            pass
    if profile_model:
        user_field = profile_model._meta.get_field_by_name('user')[0]
        related_name = user_field.related_query_name()
        profile_prefix = '%s__' % related_name
        for k in kwargs.keys():
            if k.startswith(profile_prefix):
                profile_key = k.replace(profile_prefix, '', 1)
                profile_kwargs[profile_key] = kwargs.pop(k)

    # create the user
    user = cls._default_manager.create(**kwargs)

    if profile_model and profile_kwargs:
        # update or create the profile model
        profile, created = profile_model._default_manager.get_or_create(
            user=user, defaults=profile_kwargs)
        if not created:
            for k, v in profile_kwargs.items():
                setattr(profile, k, v)
            profile.save()
        setattr(user, related_name, profile)
        setattr(user, '_profile_cache', profile)

    return user

UserF.set_creation_function(user_create)


def ct_get_model(app_label):
    try:
        app_models = __import__("%s.%s" % (app_label, 'models'), {}, {}, ['*'])
    except ImportError:
        return None

    for prop in dir(app_models):
        attr = getattr(app_models, prop)
        try:
            if issubclass(attr, Model):
                return attr
        except TypeError:
            pass  # not a class at all.
    else:
        return None


class ContentTypeF(factory.Factory):
    FACTORY_FOR = ctmodels.ContentType

    name = factory.Sequence(lambda n: "content type %s" % n)

    @factory.lazy_attribute
    def app_label(a):
        for label_maybe in settings.INSTALLED_APPS:
            model = ct_get_model(label_maybe)
            if not model is None:
                # avoid returning a model which is imported into this app, but
                #  not actually part of this app
                if label_maybe.endswith(model._meta.app_label):
                    return label_maybe
        else:
            raise ValueError(
                "No INSTALLED_APP has a model; please do that before trying to construct a ContentTypeF.")

    @factory.lazy_attribute
    def model(a):
        return ct_get_model(a.app_label)


def CTF_create(cls, **kwargs):
    app_label = kwargs.pop('app_label')
    model = kwargs.pop('model')
    return ctmodels.ContentType.objects.get_or_create(
        app_label=app_label,
        model=model._meta.module_name, defaults=kwargs)[0]

ContentTypeF.set_creation_function(CTF_create)


class PermissionF(factory.Factory):
    FACTORY_FOR = models.Permission

    name = factory.Sequence(lambda n: "permission%s" % n)
    content_type = factory.SubFactory(ContentTypeF)
    codename = factory.Sequence(lambda n: "factory_%s" % n)
