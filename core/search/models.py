from django.db import models


class SearchableTool(models.Model):
    name = models.CharField(max_length=255, unique=True)
    link = models.CharField(max_length=2048)
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"%s" % self.name
