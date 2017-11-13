from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^topics/?$', views.topic_list,
        name='ranker_topics'),
    url(r'^topics/(?P<topic_id>[1-9][0-9]*)/?$', views.topic_detail,
        name='ranker_topic_detail'),
    url(r'^topics/(?P<topic_id>[1-9][0-9]*)/options/?$', views.topic_option_list,
        name='ranker_topic_options'),
    url(r'^topics/(?P<topic_id>[1-9][0-9]*)/options/(?P<option_id>[1-9][0-9]*)/?$',
        views.topic_option_detail, name='ranker_topic_option_detail'),
    url(r'^topics/(?P<topic_id>[1-9][0-9]*)/contests/?$', views.contest_manager,
        name='ranker_topic_contest'),
    url(r'^topics/(?P<topic_id>[1-9][0-9]*)/rankings/?$', views.topic_rankings,
        name='ranker_topic_rankings'),
    url(r'^options/?$', views.option_list, name='ranker_options'),
    url(r'^options/(?P<option_id>[1-9][0-9]*)/?$', views.option_detail,
        name='ranker_option_detail'),
]
