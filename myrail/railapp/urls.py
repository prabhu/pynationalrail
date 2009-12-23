from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('railapp.views',
    url(r'^$', 'app_default', name='app-default'),
    url(r'^d/$', 'departures', name='departures'),
    url(r'^a/$', 'arrivals', name='arrivals'),
    url(r'^s/$', 'service', name='service'),
    url(r'^f/$', 'favorites', name='favorites'),
    url(r'^fs/$', 'favorites_search', name='favorites-search'),
    url(r'^r/$', 'recent', name='recent'),
    url(r'^login/$', 'loginAction', name='login'),
    url(r'^j/$', 'journeyPlanner', name='journeyPlanner'),
)
