from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^search/companies/$',
        views.CompanySearchView.as_view(),
        name='search-companies'
    ),
]
