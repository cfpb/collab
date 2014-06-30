from django.db import models
from core.notifications.email import email_notification
from django.conf import settings
import uuid


class Notification(models.Model):

    """
        Notification for users that some action has happened, like they
        were tagged by another user.
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
    uuid = models.CharField(max_length=255)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
    verb = models.TextField(max_length=255)
    obj = models.TextField("message representing notification.")
    target = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='user_notifications')
    title = models.TextField(max_length=255)
    viewed = models.BooleanField(default=False)
    url = models.TextField(max_length=255, blank=True, null=True)

    def save(self):
        """Overriding save in order to generate UUID as a primary key."""
        if not self.pk:
            self.uuid = uuid.uuid4()
        super(Notification, self).save()

    def __unicode__(self):
        """
        Simple to_string representation of notification object.
        """
        return '(%s) %s said to %s "%s"' % (self.uuid,
                                            self.owner, self.actor, self.obj)

    @classmethod
    def set_notification(cls, owner, actor, verb, obj, target, title, url=None, email_info=None):
        """
        Add notification to database and email if user allows.

        """
        n = cls(owner=owner,
                actor=actor,
                verb=verb,
                obj=obj,
                target=target,
                title=title,
                url=url,
                )
        n.save()

        if target.get_profile().email_notifications and email_info is not None:
            email_notification(n, email_info)

        return n

    @classmethod
    def mark_all_read(cls, user):
        """
        Mark all notifications as read for a given user

        @param: L{User}

        """
        try:
            notifications = cls.objects.filter(
                target=user).filter(viewed=False)
            for n in notifications:
                n.viewed = True
                n.save()
            return True
        except:
            return False

    @classmethod
    def mark_one_read(cls, user, uuid):
        """
        Mark a single notification as read

        @param: L{User}
        @param: A string UUID/primary key to a L{Notification} object

        """
        try:
            n = cls.objects.filter(uuid=uuid).filter(target=user)[0]
            n.viewed = True
            n.save()
        except:
            return False

    @classmethod
    def get_unread(cls, user):
        """
        Returns list of unread notifications for a given user
        @param: L{User}
        """
        unviewed = cls.objects.filter(target=user).filter(
            viewed=False).order_by('-timestamp')
        return unviewed

    @classmethod
    def get_and_mark_unread(cls, user):
        """
        Returns iterator of unread notifications for a given user. Marks all as read.
        @param: L{User}
        """
        unread = cls.get_unread(user)
        notifications = [n for n in unread]
        if len(unread) > 0:
            unread.update(viewed=True)
        return notifications

    @classmethod
    def get_slice(cls, user, start_row, end_row, just_new):
        """
        Returns list of notifications ordered by date, descending
        """
        notifications = cls.objects.select_related(
            'actor').filter(target=user).order_by('-timestamp')
        if just_new:
            notifications = notifications.filter(viewed=False)
        notifications = notifications[start_row:end_row]
        return notifications
