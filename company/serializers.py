from rest_framework import serializers


class CompanySearchQuerySerializer(serializers.Serializer):

    q = serializers.CharField()


class CompanySearchResultSerializer(serializers.Serializer):
    address = serializers.DictField(
        child=serializers.CharField(allow_blank=True)
    )
    country_of_origin = serializers.CharField(allow_blank=True)
    address_snippet = serializers.CharField(allow_blank=True)
    company_name = serializers.CharField()
    company_number = serializers.CharField()
    company_status = serializers.CharField()
    company_type = serializers.CharField()
    date_of_cessation = serializers.DateField(required=False)
    date_of_creation = serializers.DateTimeField()

