from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.category_list, name='category-list'),
]
