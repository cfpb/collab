import datetime
from haystack import indexes
from core.models import Person


class PersonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    user = indexes.CharField(model_attr='user')
    org_group = indexes.CharField(model_attr='org_group', null=True)
    display = indexes.CharField(model_attr='full_name', null=True)
    description = indexes.CharField(model_attr='title', null=True)
    index_name = indexes.CharField(indexed=False)
    index_priority = indexes.IntegerField(indexed=False)
    url = indexes.CharField(indexed=False, null=True)
    image = indexes.CharField(indexed=False, null=True)

    PRIORITY = 1

    def prepare_index_name(self, obj):
        return "Staff Directory"

    def prepare_index_priority(self, obj):
        return self.PRIORITY

    def prepare_url(self, obj):
        return obj.get_absolute_url()

    def prepare_image(self, obj):
        return obj.photo_file.url_125x125

    def get_model(self):
        return Person

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(
            user__is_active=True).filter(
            hide_profile=False)
