from django.test import TestCase
from exam.decorators import before
from exam.cases import Exam
from django.core.urlresolvers import reverse
from core.search.models import SearchableTool


class SearchableToolTest(TestCase):

    def test_unicode_repr(self):
        tool = SearchableTool(name="Hello world")
        self.assertEquals(unicode(tool), "Hello world")


class SmokeTests(Exam, TestCase):
    fixtures = ['core-test-fixtures.json', ]

    @before
    def login(self):
        self.client.login(username='test1@example.com', password='1')

    def test_search_page(self):
        """
            Tests that the blank search page appears with no errors.
        """
        resp = self.client.get(reverse('search:index'))
        self.assertContains(resp, 'Search the Intranet', status_code=200)

    def test_search_tags_json_post_must_redirect(self):
        """
            Tests that the search tags json post request redirects
            to a get request.
        """
        resp = self.client.post(reverse('search:tags_json'),
                                {'term': 'xyz'})
        self.assertEquals(302, resp.status_code)

    def test_search_tags_json_get_no_results(self):
        """
            Tests that a get request on the search tags json works
            even when there are no matching results.
        """
        resp = self.client.get('/search/tags/json/?term=xyz')
        self.assertContains(resp, '{}', status_code=200)

    def test_search_tags_json_get_results(self):
        """
            Tests that a get request on the search tags json works
            and returns results.
        """
        resp = self.client.get('/search/tags/json/?term=Wonderful')
        self.assertContains(resp, '"value": "Wonderful"', status_code=200)
