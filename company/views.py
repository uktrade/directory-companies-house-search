from django.http import HttpResponseNotFound
from elasticsearch import NotFoundError
from rest_framework.response import Response
from rest_framework.views import APIView

from .doctypes import CompanyDocType
from .serializers import CompanySearchResultSerializer, \
    CompanySearchQuerySerializer, RegisteredOfficeAddressSerializer


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


class CompanyRegisteredOfficeAddress(APIView):

    def get(self, request, company_number, format=None):
        try:
            result = CompanyDocType.get(id=company_number)
        except NotFoundError:
            return HttpResponseNotFound()

        result_serializer = RegisteredOfficeAddressSerializer(
            data=result.address.to_dict()
        )
        result_serializer.is_valid()
        return Response(data=result_serializer.validated_data)
