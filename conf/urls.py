import directory_healthcheck.views

from django.conf.urls import url, include
from django.contrib import admin

import company.views
import healthcheck.views


admin.autodiscover()


company_urlpatterns = [
    url(
        r'^search/companies/$',
        company.views.CompanySearchView.as_view(),
        name='search-companies'
    ),
    url(
        r'^company/(?P<company_number>\w+)/registered-office-address/$',
        company.views.CompanyRegisteredOfficeAddress.as_view(),
        name='company-registered-office-address'
    ),
    url(
        r'^company/(?P<company_number>\w+)/$',
        company.views.CompanyProfile.as_view(),
        name='company-profile'
    ),
    url(
        r'^company/(?P<company_number>\w+)/officers/$',
        company.views.CompanyOfficers.as_view(),
        name='company-officers'
    ),
]

urlpatterns = [
    url(
        r'^admin/',
        include(admin.site.urls)
    ),
    url(
        r'^healthcheck/database/$',
        healthcheck.views.DatabaseAPIView.as_view(),
        name='healthcheck-database'
    ),
    url(
        r'^healthcheck/cache/$',
        healthcheck.views.CacheAPIView.as_view(),
        name='healthcheck-cache'
    ),
    url(
        r'^healthcheck/elasticsearch/$',
        healthcheck.views.ElasticsearchAPIView.as_view(),
        name='healthcheck-elastic-search'
    ),
    url(
        r'^healthcheck/ping/$',
        directory_healthcheck.views.PingView.as_view(),
        name='healthcheck-ping'
    ),
    url(
        r'^healthcheck/sentry/$',
        directory_healthcheck.views.SentryHealthcheckView.as_view(),
        name='healthcheck-sentry'
    ),
    url(
        r'^api/', include(company_urlpatterns, namespace='api')
    )
]
