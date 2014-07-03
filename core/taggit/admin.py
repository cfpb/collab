from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from core.taggit.models import Tag, TaggedItem, TagCategory


class TaggedItemInline(admin.StackedInline):
    model = TaggedItem


class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ('name', 'slug')
    inlines = [
        TaggedItemInline
    ]


class TaggedItemForm(forms.ModelForm):
    tag_creator = forms.ModelChoiceField(
        queryset=get_user_model().objects.order_by('username'))

    class Meta:
        model = TaggedItem


class TaggedItemAdmin(admin.ModelAdmin):
    list_display = ["tag", "tag_creator", "tag_category"]
    form = TaggedItemForm


admin.site.register(Tag, TagAdmin)
admin.site.register(TaggedItem, TaggedItemAdmin)
admin.site.register(TagCategory)
