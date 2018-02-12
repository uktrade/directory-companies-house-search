from django.http import Http404
from elasticsearch import NotFoundError
from rest_framework.response import Response
from rest_framework.views import APIView

from .doctypes import CompanyDocType
from .serializers import CompanyProfileSerializer, \
    CompanySearchResultSerializer, CompanySearchQuerySerializer, \
    RegisteredOfficeAddressSerializer


class CompanySearchView(APIView):

    def get(self, request, format=None):
        request_serializer = CompanySearchQuerySerializer(
            data=request.query_params
        )
        request_serializer.is_valid(raise_exception=True)

        search_object = CompanyDocType.search().query(
            'match_phrase',
            company_name=request_serializer.data['q']
        )
        results = self.from_ch_results_to_dicts(search_object)
        result_serializer = CompanySearchResultSerializer(
            data=results, many=True
        )
        result_serializer.is_valid(raise_exception=True)
        return Response(data=result_serializer.validated_data)

    @staticmethod
    def from_ch_results_to_dicts(search_object):
        results = []
        hits = search_object.execute().to_dict()
        for hit in hits['hits']['hits']:
            results.append(hit['_source'])

        return results


class BaseCompanyView(APIView):
    serializer_class = None

    @staticmethod
    def get_company_or_404(company_number):
        try:
            return CompanyDocType.get(id=company_number)
        except NotFoundError:
            raise Http404()

    def get_data(self, company):
        raise NotImplementedError

    def get(self, request, company_number, format=None):
        company = self.get_company_or_404(company_number)
        data = self.get_data(company)
        result_serializer = self.serializer_class(data=data)
        result_serializer.is_valid()
        return Response(data=result_serializer.validated_data)


class CompanyProfile(BaseCompanyView):
    serializer_class = CompanyProfileSerializer

    def get_data(self, company):
        company = company.to_dict()
        # in the profile Ch returns the address in a different key name
        company['registered_address'] = company['address']
        return company


class CompanyRegisteredOfficeAddress(BaseCompanyView):
    serializer_class = RegisteredOfficeAddressSerializer

    def get_data(self, company):
        return company.address.to_dict()
