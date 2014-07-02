from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'login/$', 'django.contrib.auth.views.login',
                           {'template_name': 'login.html'}, name='login'),
                       url(r'^', include('core.urls', namespace="core")),
                       url(r'^search/', include(
                           'core.search.urls', namespace="search")),
                       url(r'^stats/', include(
                           'core.stats.urls', namespace="stats")),
                       url(r'^notifications/', include(
                           'core.notifications.urls', namespace="notifications")),
                       url(r'^admin/', include(admin.site.urls)),
                       )


# only include url patterns if apps are installed
if 'aup' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^aup/', include('aup.urls', namespace="aup"))),

if 'bookmarks' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^links/', include(
        'bookmarks.urls', namespace="bookmarks"))),

if 'news' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^announcements/',
                           include('news.urls', namespace="news"))),
    urlpatterns.append(url(r'^news/(?P<idx>.+)/$',
                           RedirectView.as_view(url='/announcements/%(idx)s/')))
    urlpatterns.append(url(r'^news/$',
                           RedirectView.as_view(url='/announcements/')))

if 'ohc_pmit' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^pmit/', include(
        'ohc_pmit.urls', namespace="pmit")))

if 'design' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^design/', include(
        'design.urls', namespace="design")))

if 'examiners_encyclopedia' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^supervision/e2/',
                           include('examiners_encyclopedia.urls', namespace="e2")))

if 'resource_library' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^resource_library/',
                           include('resource_library.urls', namespace="resource_library")))
    urlpatterns.append(url(r'^supervision/e2/', RedirectView.as_view(url=reverse_lazy(
        "resource_library:by_category", args=('examiners-encyclopedia',)))))

if 'staff_directory' in settings.INSTALLED_APPS:
    urlpatterns.append(
        url(r'^staff/', include(
            'staff_directory.urls', namespace="staff_directory")),
    )

if 'meta_data' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^metadata/', include(
        'meta_data.urls', namespace="meta_data")))

if 'form_builder' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^forms/', include(
        'form_builder.urls', namespace="form_builder")))

if 'welcome' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^welcome/', include(
        'welcome.urls', namespace="welcome")))

if 'github_dashboard' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^dashboard/dev/', include(
        'github_dashboard.urls', namespace="github")))

if 'idea' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^idea/', include(
        'idea.urls', namespace="idea")))

if 'whats_new' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^whats_new/', include(
        'whats_new.urls', namespace="whats_new")))

if 'press_clips' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^press_clips/', include(
        'press_clips.urls', namespace="press_clips")))

if 'mystery' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^mystery/', include(
        'mystery.urls', namespace="mystery")))

if 'wizwiz' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^dtree/', include(
        'wizwiz.urls', namespace="wiz")))

if 'django.contrib.comments' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^comments/',
        include('django.contrib.comments.urls')))
