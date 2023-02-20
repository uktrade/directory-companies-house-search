from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from .data import CompaniesHouseException, DataLoader
from .serializers import CompanyProfileSerializer, \
    CompanySearchResultSerializer, CompanySearchQuerySerializer, \
    RegisteredOfficeAddressSerializer


class CompanySearchView(APIView):

    @extend_schema(
        request=CompanySearchQuerySerializer,
        responses={200: CompanySearchResultSerializer},
    )
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
        return Response(data=self.serialize_data(data))

    def serialize_data(self, data):
        result_serializer = self.serializer_class(data=data)
        result_serializer.is_valid(raise_exception=True)
        return result_serializer.validated_data


class CompanyProfile(BaseCompanyView):
    serializer_class = CompanyProfileSerializer

    def get_data(self, company_number):
        return DataLoader().retrieve_profile(company_number=company_number)


class CompanyRegisteredOfficeAddress(BaseCompanyView):
    serializer_class = RegisteredOfficeAddressSerializer

    def get_data(self, company_number):
        return DataLoader().retrieve_address(company_number=company_number)


class CompanyOfficers(BaseCompanyView):

    def serialize_data(self, data):
        return data

    def get_data(self, company_number):
        return DataLoader().list_officers(company_number=company_number)

    def handle_exception(self, exception):
        if isinstance(exception, CompaniesHouseException):
            if exception.status_code == 404:
                return Response(status=404)
        return super().handle_exception(exception)
