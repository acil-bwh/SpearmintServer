from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^show/(?P<name>.+)/$', views.show, name='show'),
    url(r'^delete/(?P<name>.+)/$', views.delete, name='delete'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^token/$', views.token, name='token'),
    url(r'^message/$', views.message, name='message'),
]

app_name = 'app'