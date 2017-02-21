import re

from django.conf import settings
from django.db import models


class SearchableTool(models.Model):
    name = models.CharField(max_length=255, unique=True)
    link = models.CharField(max_length=2048)
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"%s" % self.name


class SuggestedSearchResult(models.Model):

    search_term = models.CharField(max_length=255)
    suggested_url = models.URLField()
    description = models.TextField()

    def __unicode__(self):
        return u"%s" % self.search_term

    def to_dict(self):
        name = re.sub(r"(?i)^https://.+?/", "/", self.suggested_url)
        name = name.replace(settings.WIKI_HOME + '/', '').replace('_', ' ').replace('#', ': ')

        return {'search_term': self.search_term,
                'suggested_url': self.suggested_url,
                'name': name,
                'description': self.description}
