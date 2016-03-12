from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'special_random.views.home', name='home'),
    # url(r'^special_random/', include('special_random.foo.urls')),


    url(r'^$', 'special_random.main.views.index', name="index"),
    url(r'^qualifying/$', 'special_random.main.views.qualifying', name="qualifying"),
    url(r'^qualifying/(?P<diff>.*)/$', 'special_random.main.views.qualifying_d', name="qualifying_d"),
    url(r'^qualifying_q/(?P<diff>.*)/(?P<pk>.*)/$', 'special_random.main.views.qualifying_q', name="qualifying_q"),
    url(r'^qualifying_q/(?P<diff>.*)/$', 'special_random.main.views.qualifying_q', name="qualifying_q"),

    url(r'^main/$', 'special_random.main.views.main', name="main"),
    url(r'^main/(?P<pk>.*)/$', 'special_random.main.views.main', name="main"),
    url(r'^main/(?P<pk>.*)/(?P<take_pk>.*)$', 'special_random.main.views.main', name="main"),
    url(r'^main_play/(?P<pk>.*)$', 'special_random.main.views.main_play', name="main_play"),

    url(r'^third/$', 'special_random.main.views.third', name="third"),
    url(r'^third/(?P<pk>.*)/$', 'special_random.main.views.third', name="third"),
    url(r'^third/(?P<pk>.*)/(?P<take_pk>.*)$', 'special_random.main.views.third', name="third"),

    # url(r'^set/(?P<set_pk>.*)/$', 'special_random.main.views.set', name="set"),
    # url(r'^random/(?P<set_pk>.*)/(?P<group_pk>.*)/$', 'special_random.main.views.random', name="random"),
    # url(r'^real_random/(?P<take_pk>.*)/(?P<ban_pk>.*)/(?P<player_pk>.*)/$', 'special_random.main.views.real_random', name="real_random"),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

