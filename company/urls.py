from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^search/companies/$',
        views.CompanySearchView.as_view(),
        name='search-companies'
    ),
    url(
        r'^company/(?P<company_number>.*)/registered-office-address/$',
        views.CompanyRegisteredOfficeAddress.as_view(),
        name='company-registered-office-address'
    )
]
