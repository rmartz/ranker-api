from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.category_list, name='category-list'),
    url(r'^(?P<category>[0-9]+)/$', views.category_detail, name='category-detail'),
    url(r'^(?P<category>[0-9]+)/topics/$', views.topic_list, name='topic-list'),
    url(r'^(?P<category>[0-9]+)/topics/(?P<topic>[0-9]+)/$', views.topic_detail, name='topic-detail'),
    url(r'^(?P<category>[0-9]+)/topics/(?P<topic>[0-9]+)/options$', views.option_list, name='topic-options-list'),
    url(r'^(?P<category>[0-9]+)/options/$', views.option_list, name='option-list'),
    url(r'^(?P<category>[0-9]+)/options/(?P<option>[0-9]+)/$', views.option_detail, name='option-detail'),
    url(r'^(?P<category>[0-9]+)/options/(?P<option>[0-9]+)/topics$', views.topic_list, name='option-topics-list'),
]
