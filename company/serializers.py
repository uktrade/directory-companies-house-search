from rest_framework import serializers


class CompanySearchQuerySerializer(serializers.Serializer):

    q = serializers.CharField()


class RegisteredOfficeAddressSerializer(serializers.Serializer):
    address_line_1 = serializers.CharField(required=False, allow_blank=True)
    address_line_2 = serializers.CharField(required=False, allow_blank=True)
    country = serializers.CharField(required=False, allow_blank=True)
    locality = serializers.CharField(required=False, allow_blank=True)
    po_box = serializers.CharField(required=False, allow_blank=True)
    postal_code = serializers.CharField(required=False, allow_blank=True)
    region = serializers.CharField(required=False, allow_blank=True)
    care_of = serializers.CharField(required=False, allow_blank=True)
    premises = serializers.CharField(required=False, allow_blank=True)


class CompanySerializer(serializers.Serializer):
    address_snippet = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    company_name = serializers.CharField()
    company_number = serializers.CharField()
    company_status = serializers.CharField()
    date_of_cessation = serializers.DateField(required=False)
    date_of_creation = serializers.DateField(required=False)


class CompanySearchResultSerializer(CompanySerializer):
    title = serializers.CharField()
    company_type = serializers.CharField()
    address = serializers.DictField(
        child=serializers.CharField(allow_blank=True)
    )


class CompanyProfileSerializer(CompanySerializer):
    type = serializers.CharField()
    registered_office_address = RegisteredOfficeAddressSerializer()
