from django.contrib import admin
from core.search.models import SearchableTool
from core.search.models import SuggestedSearchResult

admin.site.register(SearchableTool)
admin.site.register(SuggestedSearchResult)
