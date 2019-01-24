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
    sic_codes = field.Text()

    class Meta:
        index = settings.ELASTICSEARCH_COMPANY_INDEX_ALIAS

    def to_dict(self, include_meta=False):
        meta = super().to_dict(include_meta)
        if '_source' in meta:
            company = meta['_source']
            company['title'] = company['company_name']
            company['address']['country'] = company['country_of_origin']
            company['company_type'] = company['type']
            meta['_source'] = self.reformat_date(company)
        return meta

    def to_profile_dict(self):
        company = self.to_dict()
        company['registered_office_address'] = company['address']
        return self.reformat_date(company)

    @staticmethod
    def reformat_date(company):
        if 'date_of_creation' in company:
            company['date_of_creation'] = company[
                'date_of_creation'].strftime('%Y-%m-%d')
        if 'date_of_cessation' in company:
            company['date_of_cessation'] = company[
                'date_of_cessation'].strftime('%Y-%m-%d')
        return company
