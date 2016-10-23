from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.category_list, name='category-list'),
    url(r'^(?P<id>[0-9]+)/$', views.category_detail, name='category-detail'),
]
