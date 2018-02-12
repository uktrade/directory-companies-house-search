from django.core.management import BaseCommand
from elasticsearch.helpers import bulk
from elasticsearch_dsl.index import connections, Index

from django.conf import settings

from company.utils import create_company_document, open_zipped_csv
from .import_ch_companies import CH_CSV_FIELDNAMES


class Command(BaseCommand):
    help = "Load CH companies test data in Elasticsearch"
    company_index_alias = settings.ELASTICSEARCH_COMPANY_INDEX_ALIAS

    def companies_from_csv(self, file_object):
        """Fetch & cache zipped CSV, and then iterate though contents."""
        with open_zipped_csv(file_object, CH_CSV_FIELDNAMES) as csv_reader:
            next(csv_reader)  # skip the csv header
            for row in csv_reader:
                yield create_company_document(row)

    def populate_new_index(self):
        client = connections.get_connection()
        with open('company/tests/ch_part1_2.zip', 'rb') as zipped_csv:
            companies = self.companies_from_csv(zipped_csv)
            companies_dicts = (company.to_dict(True) for company in companies)

            bulk(
                client,
                companies_dicts,
                chunk_size=100,
                raise_on_exception=True
                )

    def refresh_index(self):
        Index(self.company_index_alias).refresh()

    def handle(self, *args, **options):
        self.populate_new_index()
        self.refresh_index()
