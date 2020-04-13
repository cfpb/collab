import os
from django.test import TestCase
from django_webtest import WebTest
from exam.decorators import fixture
from exam.cases import Exam
from collab.django_factories import UserF
from core.models import OrgGroup, Person


class ViewTest(Exam, WebTest):
    fixtures = ['core-test-fixtures.json', ]

    @fixture
    def user(self):
        """
            Create a user without a profile and set the email
            to blank (what we get from Kerberos)
        """
        user = UserF.build()
        user.email = ''
        user.save()
        return user

    def get(self, url):
        return self.app.get(url, user=self.user)

    def fill_form(self, form):
        form['first_name'] = self.user.first_name
        form['last_name'] = self.user.last_name
        form['title'] = 'Djangonaut'
        form['email'] = 'user12@example.com'
        form['office_phone'] = '5553332222'
        form.set('org_group', OrgGroup.objects.all()[0].pk)
        form.set('office_location', 'DC123')
        return form

    def test_register_with_good_data(self):
        with self.assertRaises(Person.DoesNotExist):
            self.user.get_profile()

        page = self.get('/').follow()
        form = page.form

        form = self.fill_form(form)
        result = form.submit().follow()

        self.assertIsInstance(self.user.get_profile(), Person)

        assert self.user.get_profile().title == 'Djangonaut'
        assert self.user.get_profile().office_location_id == 'DC123'
        assert self.user.get_profile().photo_file == 'avatars/default.jpg'

    def test_register_with_bad_data(self):
        page = self.get('/').follow()
        form = page.form
        form = self.fill_form(form)
        form['email'] = ""
        result = form.submit()

        assert "errorlist" in result

    def test_register_with_avatar(self):
        page = self.get('/').follow()
        form = page.form
        form = self.fill_form(form)
        file_path = os.path.join(os.path.realpath(
            os.path.dirname(__file__)), 'files', 'fff.png')
        form.set('photo_file', ('fff.png', file(file_path).read()))
        result = form.submit().follow()

        assert str(self.user.get_profile().photo_file).find('fff') > 0
