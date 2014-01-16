import datetime
from haystack import indexes
from core.taggit.models import Tag


class TagIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    name = indexes.EdgeNgramField(model_attr='name', null=True)
    display = indexes.CharField(model_attr='name', null=True)
    index_name = indexes.CharField(indexed=False)
    index_priority = indexes.IntegerField(indexed=False)
    url = indexes.CharField(indexed=False, null=True)

    PRIORITY = 2

    def prepare_index_name(self, obj):
        return "Staff Directory"

    def prepare_index_priority(self, obj):
        return self.PRIORITY

    def prepare_url(self, obj):
        return obj.get_absolute_url()

    def prepare_display(self, obj):
        return "Tag: %s" % obj.name

    def get_model(self):
        return Tag

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
