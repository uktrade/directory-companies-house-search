from django.conf.urls import url, include
from django.contrib import admin

import healthcheck.views


admin.autodiscover()


urlpatterns = [
    url(
        r'^admin/',
        include(admin.site.urls)
    ),
    url(
        r'^healthcheck/database/$',
        healthcheck.views.DatabaseAPIView.as_view(),
        name='health-check-database'
    ),
    url(
        r'^healthcheck/cache/$',
        healthcheck.views.CacheAPIView.as_view(),
        name='health-check-cache'
    ),
    url(
        r'^healthcheck/elasticsearch/$',
        healthcheck.views.ElasticsearchAPIView.as_view(),
        name='health-check-elastic-search'
    ),
    url(
        r'^healthcheck/ping/$',
        healthcheck.views.PingAPIView.as_view(),
        name='health-check-ping'
    )
]
