from company import serializers


def test_company_serializer_no_address():
    serializer = serializers.CompanySerializer(data={'address': None})

    serializer.is_valid()

    assert 'address' not in serializer.errors


def test_company_serializer_no_date_of_creation():
    serializer = serializers.CompanySerializer(data={})

    serializer.is_valid()

    assert 'date_of_creation' not in serializer.errors
