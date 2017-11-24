from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'options', views.OptionViewSet, 'ranker-options')
router.register(r'topics', views.TopicViewSet, 'ranker-topics')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^topics/(?P<topic_id>[1-9][0-9]*)/options/(?P<option_id>[1-9][0-9]*)/?$',
        views.topic_option_detail, name='ranker-topics-option-detail'),
    url(r'^topics/(?P<topic_id>[1-9][0-9]*)/contests/?$', views.contest_manager,
        name='ranker-topics-contest'),
    url(r'^topics/(?P<topic_id>[1-9][0-9]*)/rankings/?$', views.topic_rankings,
        name='ranker-topics-rankings'),
]
