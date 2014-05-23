"""
    Django Models related to central aspects of the Intranet, such as
    employee profiles and front page updates.
"""
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from collab.settings import INSTALLED_APPS
from django.db import models
from core.thumbs import ImageWithThumbsField
from core.taggit.managers import TaggableManager
from cache_tools.models import KeyableModel
from cache_tools.tools import expire_page
from django.core.urlresolvers import reverse
from core.helpers import format_phone_number
import datetime
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


class Person(KeyableModel):

    """
        Represents a user's profile
    """
    user = models.OneToOneField(User)
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
    tags = TaggableManager()
    start_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    @classmethod
    def active_user_count(cls):
        return User.objects.filter(is_active=True).count()

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
        if 'staff_directory' in INSTALLED_APPS:
            return expire_page(reverse('staff_directory:person', args=(self.stub,)))
        else:
            pass

    def format_phone_numbers(self):
        self.office_phone_formatted = format_phone_number(self.office_phone)
        self.mobile_phone_formatted = format_phone_number(self.mobile_phone)

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
