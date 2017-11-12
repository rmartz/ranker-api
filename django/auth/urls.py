from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^user/?$', views.user_admin, name='auth_user'),
    url(r'^user/token/?$', views.token_admin, name='auth_token'),
]
