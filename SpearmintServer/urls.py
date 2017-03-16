from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SpearmintServer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('SpearmintServer.app.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api/', include('SpearmintServer.api.urls', namespace='api')),
    url(r'^app/', include('SpearmintServer.app.urls', namespace='app')),
)
