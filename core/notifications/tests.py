from django.test import TestCase
from core.notifications.models import Notification
from django.contrib.auth import get_user_model 


class NotificationsTest(TestCase):
    fixtures = ['core-test-fixtures.json', ]

    """Test whether the method "get_and_mark_unread" updates the DB even
    if there are no new notifications"""

    def test_get_and_mark_unread_no_unread(self):
        user = get_user_model().objects.get(pk=1)
        with self.assertNumQueries(1):
            Notification.get_and_mark_unread(user)

    """Test that the notification gets marked as read after being viewed"""

    def test_get_and_mark_unread(self):
        user =  get_user_model().objects.get(pk=2)
        target = get_user_model().objects.get(pk=1)

        notification = Notification(owner=user,
                                    actor=user,
                                    verb="tagged",
                                    obj="Wonderful",
                                    target=target,
                                    title="John tagged you with \"Wonderful\"",
                                    viewed=False)
        notification.save()
        with self.assertNumQueries(2):
            Notification.get_and_mark_unread(target)
        notification = Notification.objects.get(pk=notification.pk)
        self.assertTrue(notification.viewed)

    """ Test notification gets emailed """

    def test_notification_emailed(self):
        pass

    """ Test notification shows in widget """

    def test_show_widget(self):
        pass


class ViewsTest(TestCase):
    fixtures = ['core-test-fixtures.json', ]

    """ Test marking as read action """

    def test_mark_as_read(self):
        self.client.login(username='test1@example.com', password='1')

        user = get_user_model().objects.get(pk=1)
        notification = Notification.set_notification(
            user, user, "tagged", user,
            user, "You tagged someone", "http://url.com/")
        self.assertFalse(notification.viewed)
        response = self.client.post(
            '/notifications/mark_as_read/' + str(notification.pk))
        self.assertEquals(200, response.status_code)

        notification = Notification.objects.get(pk=notification.pk)
        self.assertTrue(notification.viewed)

    """ Test marking all as read action, should only view notifications
        where the notification.target is the active user"""

    def test_mark_all_as_read(self):
        self.client.login(username='test1@example.com', password='1')
        login_user = get_user_model().objects.get(pk=1)
        other_user = get_user_model().objects.get(pk=3)
        notification1 = Notification.set_notification(
            owner=login_user, actor=login_user, verb="tagged", obj="message",
            target=login_user, title="You tagged someone",
            url="http://url.com/")
        notification2 = Notification.set_notification(
            owner=other_user, actor=other_user, verb="tagged", obj="message",
            target=login_user, title="You tagged someone",
            url="http://url.com/")
        notification3 = Notification.set_notification(
            owner=login_user, actor=login_user, verb="tagged", obj="message",
            target=other_user, title="You tagged someone",
            url="http://url.com/")
        self.assertFalse(notification1.viewed)
        self.assertFalse(notification2.viewed)
        self.assertFalse(notification3.viewed)
        response = self.client.post(
            '/notifications/mark_all_as_read/')
        self.assertEquals(200, response.status_code)

        notification1 = Notification.objects.get(pk=notification1.pk)
        notification2 = Notification.objects.get(pk=notification2.pk)
        notification3 = Notification.objects.get(pk=notification3.pk)
        self.assertTrue(notification1.viewed)
        self.assertTrue(notification2.viewed)
        self.assertFalse(notification3.viewed)
