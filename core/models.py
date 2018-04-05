"""
    Django Models related to central aspects of the Intranet, such as
    employee profiles and front page updates.
"""
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, SiteProfileNotAvailable
from django.core import validators
from django.db import models
from core.thumbs import ImageWithThumbsField
from core.taggit.managers import TaggableManager
from cache_tools.models import KeyableModel
from cache_tools.tools import expire_page
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured
from core.helpers import format_phone_number
import datetime
import re
from django.utils import timezone
from south.modelsinspector import add_ignored_fields

add_ignored_fields(["^core\.taggit\.managers\.TaggableManager"])


class App(models.Model):
    title = models.CharField(max_length=255)
    stub = models.CharField(max_length=32)
    description = models.CharField(max_length=255)
    path = models.CharField(max_length=32)
    icon_file = ImageWithThumbsField(upload_to='app_icons',
                                     sizes=(
                                         (300, 300), (200, 200), (100, 100)),
                                     default='app_icons/default.jpg',
                                     null=True,
                                     blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        permissions = (
            ("can_use", "Can use this app"),
        )

class CollabUser(AbstractBaseUser, PermissionsMixin):
    ''' Override base User class to increases username limit to 75 '''
    username = models.CharField(max_length=75, unique=True,
        help_text='Required. 75 characters or fewer. Letters, numbers and ' +
                  "@/./'/+/-/_ characters",
        validators=[
            validators.RegexValidator(re.compile("^[\w.'@+-]+$"),
                                      'Enter a valid username.', 'invalid')
        ])
    first_name = models.CharField(max_length=75, blank=True)
    last_name = models.CharField(max_length=75, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    is_staff = models.BooleanField(default=False,
        help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField(default=True,
        help_text='Designates whether this user should be treated as ' +
                  'active. Unselect this instead of deleting accounts.')

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def get_profile(self):
        """
        Returns site-specific profile for this user. Raises
        SiteProfileNotAvailable if this site does not allow profiles.
        """
        if not hasattr(self, '_profile_cache'):
            if not getattr(settings, 'AUTH_PROFILE_MODULE', False):
                raise SiteProfileNotAvailable(
                    'You need to set AUTH_PROFILE_MODULE in your project '
                    'settings')
            try:
                app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
            except ValueError:
                raise SiteProfileNotAvailable(
                    'app_label and model_name should be separated by a dot in '
                    'the AUTH_PROFILE_MODULE setting')
            try:
                model = models.get_model(app_label, model_name)
                if model is None:
                    raise SiteProfileNotAvailable(
                        'Unable to load the profile model, check '
                        'AUTH_PROFILE_MODULE in your project settings')
                self._profile_cache = model._default_manager.using(
                                   self._state.db).get(user__id__exact=self.id)
                self._profile_cache.user = self
            except (ImportError, ImproperlyConfigured):
                raise SiteProfileNotAvailable
        return self._profile_cache


class Person(KeyableModel):

    """
        Represents a user's profile
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    stub = models.CharField(max_length=128, null=True, blank=True)
    title = models.CharField(max_length=128, null=True, blank=True)
    org_group = models.ForeignKey('OrgGroup', null=True, blank=True)
    office_location = models.ForeignKey('OfficeLocation', null=True,
                                        blank=True)
    desk_location = models.CharField(max_length=128, null=True, blank=True)
    office_phone = models.CharField(max_length=32, null=True, blank=True)
    mobile_phone = models.CharField(max_length=32, null=True, blank=True)
    home_phone = models.CharField(max_length=32, null=True, blank=True)
    photo_file = ImageWithThumbsField(upload_to='avatars',
                                      sizes=((34, 34), (125, 125), (200, 200)),
                                      default='avatars/default.jpg')
    what_i_do = models.TextField(null=True, blank=True)
    current_projects = models.TextField(null=True, blank=True)
    stuff_ive_done = models.TextField(null=True, blank=True)
    things_im_good_at = models.TextField(null=True, blank=True)
    schools_i_attended = models.TextField(null=True, blank=True)
    allow_tagging = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=False)
    hide_profile = models.BooleanField(default=False)
    tags = TaggableManager()
    start_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    @classmethod
    def active_user_count(cls):
        return get_user_model().objects.filter(is_active=True).count()

    @property
    def full_name(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    @property
    def days_since_hire(self):
        if self.start_date:
            diff = timezone.now() - self.start_date
            return diff.days
        else:
            pass

    def expire_cache(self):
        if 'staff_directory' in settings.INSTALLED_APPS:
            return expire_page(reverse('staff_directory:person', args=(self.stub,)))
        else:
            pass

    def format_phone_numbers(self):
        self.office_phone_formatted = format_phone_number(self.office_phone)
        self.mobile_phone_formatted = format_phone_number(self.mobile_phone)
        self.home_phone_formatted = format_phone_number(self.home_phone)

    def save(self, *args, **kwargs):
        if self.photo_file is None:
            self.photo_file = 'avatars/default.jpg'
        self.expire_cache()
        self.format_phone_numbers()
        super(Person, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.user

    def get_absolute_url(self):
        return reverse('staff_directory:person', args=(self.stub,))

    # Search fields

    @classmethod
    def search_category(cls):
        return 'Staff Directory'

    @property
    def to_search_result(self):
        return self.full_name


class OrgGroup(models.Model):

    """
        Represents a user's office and team.  It can also represent
        an organization hierarchy.
    """
    title = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True)

    def __unicode__(self):
        return self.title


class OfficeLocation(models.Model):

    """
        Represents a CFPB office.  Details with respect to room number or
        office number, floor, etc., are intentionally omitted
    """
    id = models.CharField(max_length=12, primary_key=True)
    name = models.CharField(max_length=56)
    street = models.CharField(max_length=56)
    suite = models.CharField(max_length=56, blank=True, null=True)
    city = models.CharField(max_length=56)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)

    def __unicode__(self):
        return '%s, %s, %s %s' % (self.street, self.city,
                                  self.state, self.zip)


class Alert(models.Model):

    """
        Provides a way to show an agency-wide alert.
    """
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=255)
    is_active = models.BooleanField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"%s" % (self.title,)
