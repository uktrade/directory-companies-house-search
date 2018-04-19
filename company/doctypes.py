from django.conf import settings
from elasticsearch_dsl import field, DocType


class CompanyDocType(DocType):
    address = field.Nested(
        properties={
            'care_of': field.Text(),
            'po_box': field.Text(),
            'address_line_1': field.Text(),
            'address_line_2': field.Text(),
            'locality': field.Text(),
            'region': field.Text(),
            'country': field.Text(),
            'postal_code': field.Text()
        }
    )
    country_of_origin = field.Text()
    address_snippet = field.Text()
    company_name = field.Text()
    company_number = field.Text()
    company_status = field.Text()
    type = field.Text()
    date_of_cessation = field.Date()
    date_of_creation = field.Date()

    class Meta:
        index = settings.ELASTICSEARCH_COMPANY_INDEX_ALIAS
