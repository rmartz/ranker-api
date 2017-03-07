from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^topics/?$', views.topic_list),
    url(r'^topics/([1-9][0-9]*)/?$', views.topic_detail),
    url(r'^options/?$', views.option_list),
    url(r'^options/([1-9][0-9]*)/?$', views.option_detail),
]
