from django.conf import settings
from elasticsearch_dsl import field, Document


class CompanyDocument(Document):
    address = field.Nested(
        properties={
            'care_of': field.Keyword(index=False, store=True),
            'po_box': field.Keyword(index=False, store=True),
            'address_line_1': field.Keyword(index=False, store=True),
            'address_line_2': field.Keyword(index=False, store=True),
            'locality': field.Keyword(index=False, store=True),
            'region': field.Keyword(index=False, store=True),
            'country': field.Keyword(index=False, store=True),
            'postal_code': field.Keyword(index=False, store=True)
        }
    )
    country_of_origin = field.Keyword(index=False, store=True)
    address_snippet = field.Keyword(index=False, store=True)
    company_name = field.Text()
    company_number = field.Text()
    company_status = field.Keyword(index=False, store=True)
    type = field.Keyword(index=False, store=True)
    date_of_cessation = field.Date(index=False, format='yyyy-MM-dd')
    date_of_creation = field.Date(index=False, format='yyyy-MM-dd')
    sic_codes = field.Keyword(index=False, store=True)

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
            company['date_of_creation'] = (
                company['date_of_creation'].strftime('%Y-%m-%d')
            )
        if 'date_of_cessation' in company:
            company['date_of_cessation'] = (
                company['date_of_cessation'].strftime('%Y-%m-%d')
            )
        return company
