import directory_healthcheck.views

from django.conf.urls import url, include
from django.contrib import admin

import company.views


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
        r'^healthcheck/$',
        directory_healthcheck.views.HealthcheckView.as_view(),
        name='healthcheck'
    ),
    url(
        r'^healthcheck/ping/$',
        directory_healthcheck.views.PingView.as_view(),
        name='ping'
    ),
    url(
        r'^api/', include(company_urlpatterns, namespace='api')
    )
]
