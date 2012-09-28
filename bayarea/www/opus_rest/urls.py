from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^rest/$', 'rest.views.index'),
    url(r'^rest/(?P<run_id>\d+)/$', 'rest.views.run'),
)
