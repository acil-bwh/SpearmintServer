from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^find_experiment/$', views.find_experiment, name='find_experiment'),
    url(r'^find_all_experiments/$', views.find_all_experiments, name='find_all_experiments'),
    url(r'^create_experiment/$', views.create_experiment, name='create_experiment'),
    url(r'^delete_experiment/$', views.delete_experiment, name='delete_experiment'),
    url(r'^get_suggestion/$', views.get_suggestion, name='get_suggestion'),
    url(r'^get_next_job_id/$', views.get_next_job_id, name='get_next_job_id'),
    url(r'^post_update/$', views.post_update, name='post_update'),
    url(r'^find_jobs/$', views.find_jobs, name='find_jobs'),
    url(r'^get_mongodb_uri/$', views.get_mongodb_uri, name='get_mongodb_uri'),
)
