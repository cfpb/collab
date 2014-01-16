from django.test import TestCase
from mock import Mock, MagicMock, PropertyMock
from collab.middleware import CheckForProfile
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect


class CheckForProfileTest(TestCase):

    def setUp(self):
        self.middle = CheckForProfile()
        self.request = Mock()
        self.request.session = {}
        self.request.user = MagicMock()

    def test_with_passtrhough_path(self):
        # Setup with no profile
        self.request.user.get_profile = PropertyMock(
            side_effect=ObjectDoesNotExist)

        self.request.path = reverse('core:register')
        ret = self.middle.process_request(self.request)
        self.assertEqual(ret, None)

    def test_with_widget_path(self):
        # Setup with no profile
        self.request.user.get_profile = PropertyMock(
            side_effect=ObjectDoesNotExist)

        self.request.path = '/user_widget/'
        ret = self.middle.process_request(self.request)
        self.assertEqual(ret, None)

    def test_without_profile(self):
        # Setup with no profile
        self.request.user.get_profile = PropertyMock(
            side_effect=ObjectDoesNotExist)

        self.request.path = '/'
        ret = self.middle.process_request(self.request)
        self.assertIsInstance(ret, HttpResponseRedirect)

    def test_with_profile(self):
        # Setup with profile
        self.request.user.get_profile.return_value = True
        self.request.path = '/'
        ret = self.middle.process_request(self.request)
        self.assertEqual(ret, None)
