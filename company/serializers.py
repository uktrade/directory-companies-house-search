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


class RegisteredOfficeAddressSerializer(serializers.Serializer):
    address_line_1 = serializers.CharField(allow_blank=True)
    address_line_2 = serializers.CharField(allow_blank=True)
    country = serializers.CharField(allow_blank=True)
    locality = serializers.CharField(allow_blank=True)
    po_box = serializers.CharField(allow_blank=True)
    postal_code = serializers.CharField(allow_blank=True)
    region = serializers.CharField(allow_blank=True)
    care_of = serializers.CharField(allow_blank=True)
