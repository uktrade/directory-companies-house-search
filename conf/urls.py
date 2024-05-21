import directory_healthcheck.views

from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.auth.decorators import login_required
from django.conf import settings

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

import company.views
import healthcheck.pingdom.views


admin.autodiscover()


company_urlpatterns = [
    re_path(
        r'^search/companies/$',
        company.views.CompanySearchView.as_view(),
        name='search-companies',
    ),
    re_path(
        r'^company/(?P<company_number>\w+)/registered-office-address/$',
        company.views.CompanyRegisteredOfficeAddress.as_view(),
        name='company-registered-office-address'
    ),
    re_path(
        r'^company/(?P<company_number>\w+)/$',
        company.views.CompanyProfile.as_view(),
        name='company-profile'
    ),
    re_path(
        r'^company/(?P<company_number>\w+)/officers/$',
        company.views.CompanyOfficers.as_view(),
        name='company-officers',

    ),
]

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(
        r'^healthcheck/$',
        directory_healthcheck.views.HealthcheckView.as_view(),
        name='healthcheck'
    ),
    re_path(
        r'^healthcheck/ping/$',
        directory_healthcheck.views.PingView.as_view(),
        name='ping'
    ),
    re_path(
        r'^pingdom/ping.xml',
        healthcheck.pingdom.views.PingDomView.as_view(),
        name='pingdom',
    ),
    re_path(
        r'^api/', include((company_urlpatterns, 'api'), namespace='api')
    )
]

if settings.FEATURE_OPENAPI_ENABLED:
    urlpatterns += [
        path('openapi/', SpectacularAPIView.as_view(), name='schema'),
        path(
            'openapi/ui/',
            login_required(SpectacularSwaggerView.as_view(url_name='schema'), login_url='admin:login'),
            name='swagger-ui'
        ),
        path(
            'openapi/ui/redoc/',
            login_required(SpectacularRedocView.as_view(url_name='schema'), login_url='admin:login'),
            name='redoc'
        ),
    ]
