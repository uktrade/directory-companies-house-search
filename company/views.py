from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from .data import DataLoader
from .serializers import CompanyProfileSerializer, \
    CompanySearchResultSerializer, CompanySearchQuerySerializer, \
    RegisteredOfficeAddressSerializer


class CompanySearchView(APIView):

    def get(self, request, format=None):
        request_serializer = CompanySearchQuerySerializer(
            data=request.query_params
        )
        request_serializer.is_valid(raise_exception=True)
        query = request_serializer.validated_data['q']
        results = DataLoader().search(query=query)
        result_serializer = CompanySearchResultSerializer(
            data=results, many=True
        )
        result_serializer.is_valid(raise_exception=True)
        return Response(data={'items': result_serializer.validated_data})


class BaseCompanyView(APIView):
    serializer_class = None

    def get_data(self, company_number):
        raise NotImplementedError

    def get(self, request, company_number, format=None):
        data = self.get_data(company_number)
        if not data:
            raise Http404()
        result_serializer = self.serializer_class(data=data)
        result_serializer.is_valid()
        return Response(data=result_serializer.validated_data)


class CompanyProfile(BaseCompanyView):
    serializer_class = CompanyProfileSerializer

    def get_data(self, company_number):
        return DataLoader().retrieve_profile(company_number=company_number)


class CompanyRegisteredOfficeAddress(BaseCompanyView):
    serializer_class = RegisteredOfficeAddressSerializer

    def get_data(self, company_number):
        return DataLoader().retrieve_address(company_number=company_number)
