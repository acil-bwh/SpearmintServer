from django.conf.urls import patterns, include, url
from app import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^show/(?P<name>.+)/$', views.show, name='show'),
    url(r'^delete/(?P<name>.+)/$', views.delete, name='delete'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^token/$', views.token, name='token'),
    url(r'^message/$', views.message, name='message'),
)
