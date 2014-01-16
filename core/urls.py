from django.conf.urls import patterns, url


urlpatterns = patterns('core.views',
                       url(r'^$', 'main', name='landing_page'),
                       url(r'^register/$', 'register', name='register'),
                       url(r'^account/', 'account', name='account'),
                       url(r'^user_widget/',
                           'user_widget', name='user_widget'),
                       url(r'^user_info/',
                           'user_info', name='user_info'),
                       )
