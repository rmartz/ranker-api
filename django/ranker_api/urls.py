from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^api/', include('categorizer.urls')),
    url(r'^auth/', include('auth.urls')),
    url(r'^admin/', admin.site.urls),
]
