from django.contrib import admin
from django.contrib.auth.models import User, Permission
from django.contrib.auth.admin import UserAdmin
from core.models import App, Person, OrgGroup, OfficeLocation
from core.models import Alert
from actions import export_as_csv_action


admin.site.register(OfficeLocation)
admin.site.register(App)
admin.site.register(OrgGroup)
admin.site.register(Permission)
admin.site.unregister(User)


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


class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]

admin.site.register(User, UserProfileAdmin)
admin.site.register(Alert)
