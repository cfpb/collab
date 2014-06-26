from django.test import TestCase
from django.test.utils import override_settings
from django.contrib.auth import get_user_model
from core.models import Person, App
import core.views as views
from core import helpers
import datetime
from django.utils import timezone


class PersonTest(TestCase):

    def test_format_phone_numbers_when_blank(self):
        person = Person()
        person.format_phone_numbers()
        self.assertEquals(person.office_phone_formatted, "")
        self.assertEquals(person.mobile_phone_formatted, "")

    def test_format_phone_numbers_when_not_blank(self):
        person = Person(office_phone="2025551212", mobile_phone="2025557890")
        person.format_phone_numbers()
        self.assertEquals(person.office_phone_formatted, "(202) 555-1212")
        self.assertEquals(person.mobile_phone_formatted, "(202) 555-7890")

    def test_default_avatar_when_blank(self):
        person = Person()
        self.assertEquals(person.photo_file, 'avatars/default.jpg')

    def test_default_avatar_when_not_blank(self):
        person = Person(photo_file='avatars/not_default.jpg')
        self.assertEquals(person.photo_file, 'avatars/not_default.jpg')

    def test_full_name(self):
        person = Person(user=get_user_model()(first_name="Baba", last_name="O'Reilly"))
        self.assertEquals(person.full_name, "Baba O'Reilly")

    def test_days_since_hire(self):
        person = Person(user=get_user_model()(first_name="Baba", last_name="O'Reilly"))
        person.start_date = timezone.now() - datetime.timedelta(days=10)
        self.assertEquals(person.days_since_hire, 10)


class AppTest(TestCase):

    def test_default_icon_when_blank(self):
        app = App()
        self.assertEquals(app.icon_file, 'app_icons/default.jpg')

    def test_default_icon_when_not_blank(self):
        app = App(icon_file='app_icons/not_default.jpg')
        self.assertEquals(app.icon_file, 'app_icons/not_default.jpg')


class ViewUnitTest(TestCase):

    def test_create_params_keeps_params(self):
        params = views.create_params({'hello': 'world'})
        self.assertEquals(params['hello'], 'world')

    @override_settings(WIKI_INSTALLED=True, WIKI_SEARCH_URL="http://test/%s%s")
    def test_create_params_with_wiki_installed(self):
        params = views.create_params({})
        self.assertEquals(params['wiki_installed'], True)
        self.assertEquals(
            params['wiki_search_autocomplete_json_url'], "http://test/5")


class AccessTest(TestCase):

    """
        Provides tests to make sure access privileges are required for
        all pages.
    """

    def test_access_to_index_not_logged_in(self):
        resp = self.client.get('/')
        self.assertEquals(302, resp.status_code)


class HelperUserNoProfileTest(TestCase):

    """
        Tests that the test helper function works as intended.
    """

    def test_helper_no_profile(self):
        u = get_user_model()()
        u.first_name = "John"
        u.last_name = "Smith"
        u.save()
        self.assertEquals(False, helpers.user_has_profile(u))
        p = Person()
        p.user = u
        p.save()
        self.assertEquals(True, helpers.user_has_profile(u))
