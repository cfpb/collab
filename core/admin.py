from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.auth.admin import UserAdmin
from core.models import CollabUser, App, Person, OrgGroup, OfficeLocation
from core.models import Alert
from core.forms import CollabUserChangeForm, CollabUserCreationForm
from actions import export_as_csv_action


admin.site.register(OfficeLocation)
admin.site.register(App)
admin.site.register(OrgGroup)
admin.site.register(Permission)


class CollabUserAdmin(UserAdmin):
    form = CollabUserChangeForm
    add_form = CollabUserCreationForm


class PersonAdmin(admin.ModelAdmin):
    list_display = ('user', 'stub', 'title')
    search_fields = ['title', 'stub']
    exclude = ('tags',)
    actions = [export_as_csv_action("CSV Export",
                                    fields=['full_name',
                                            'user',
                                            'title',
                                            'org_group',
                                            'office_location',
                                            'office_phone'])]


admin.site.register(Person, PersonAdmin)


class UserProfileInline(admin.StackedInline):
    model = Person
    exclude = ('tags',)


class UserProfileAdmin(CollabUserAdmin):
    inlines = [UserProfileInline]

admin.site.register(CollabUser, UserProfileAdmin)
admin.site.register(Alert)
