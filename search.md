---
layout: base
title: Search
---

## Search


Collab implements [Haystack](http://haystacksearch.org/) and establishes a few conventions, 
so no commuication is required between the apps and the core.

To show results in the search page and the autocomplete, you need to add a `search_indexes.py` file.

### Conventions

Here are the conventions Collab expects from your app:

* ``display``: The text to be shown as the title in the search results page.
* ``description``: The text to be shown as the description in the search results page.
* ``index_name`` (needs prepare): The name of the index.
* ``index_priority`` (needs prepare): Primary search priority.
* ``index_sort`` (needs prepare): Secondary search priority (optional)
* ``url`` (needs prepare): The url of the object you are indexing.

By default, collab uses index_priority to order the individual apps in the search results page.  In the example below, index_priority=1 for all Person records to ensure they all appear as a group at the top of the search results.

The secondary field, index_sort, allows an individual app to override haystacks ordering if desired.  In the example below, index_sort orders the Person records by last name.

## Example ``search_indexes.py``

    from haystack import indexes
    from core.models import Person


    class PersonIndex(indexes.SearchIndex, indexes.Indexable):
      text = indexes.EdgeNgramField(document=True, use_template=True)
      user = indexes.CharField(model_attr='user')
      display = indexes.CharField(model_attr='full_name', null=True)
      description = indexes.CharField(model_attr='title', null=True)
      index_name = indexes.CharField(indexed=False)
      index_priority = indexes.IntegerField(indexed=False)
      index_sort = indexes.IntegerField(indexed=False, null=True)
      url = indexes.CharField(indexed=False, null=True)

      PRIORITY = 1

      def prepare_index_name(self, obj):
          return "Staff Directory"

      def prepare_index_priority(self, obj):
          # Return 1 to display Staff Directory as first search result category
          return self.PRIORITY
          
      def prepare_index_sort(self, obj):
          # sort results by last name
          for index, item in enumerate(self.index_queryset().order_by("user__last_name")):
              if item.id == obj.id:
                  return index

      def prepare_url(self, obj):
          return obj.get_absolute_url()

      def get_model(self):
          return Person

      def index_queryset(self, using=None):
          """Used when the entire index for model is updated."""
          return self.get_model().objects.filter(user__is_active=True)


