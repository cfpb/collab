from django.conf.urls import patterns, url

urlpatterns = patterns('core.notifications.views',
                       url(r'^widget/$', 'widget',
                           name='widget'),
                       url(r'^mark_as_read/(?P<id>\d+)$', 'mark_as_read',
                           name='mark_as_read'),
                       url(r'^mark_all_as_read/$', 'mark_all_as_read',
                           name='mark_all_as_read'),
                       )
