from django.conf.urls import patterns, url
from django.views.generic import RedirectView

urlpatterns = patterns('core.stats.views',
                       url(r'^$', RedirectView.as_view(url='dashboard/')),
                       url(r'dashboard/$',
                           'dashboard', name='dashboard'),
                       url(r'groups/list/$',
                           'groups_list', name='groups_list'),
                       url(
                           r'groups/(?P<group_name>[^/]+)/$', 'group_users_emails',
                           name='group_users_emails'),
                       url(
                           r'staff-directory/profile-pics/$', 'staff_directory_profile_pics',
                           name='staff_directory_profile_pics'),
                       url(
                           r'users-by-division/json/$', 'users_by_division_json',
                           name='users_by_division_json'),
                       )
