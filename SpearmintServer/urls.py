from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'SpearmintServer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('SpearmintServer.app.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api/', include('SpearmintServer.api.urls', namespace='api')),
    url(r'^app/', include('SpearmintServer.app.urls', namespace='app')),
]
