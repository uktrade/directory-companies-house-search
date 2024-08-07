from opensearchpy.helpers import bulk
from opensearch_dsl.connections import connections

from django.core.management import BaseCommand
from django.conf import settings

from company import constants, documents, helpers


class Command(BaseCommand):
    help = "Load CH companies test data in Elasticsearch"
    company_index_alias = settings.OPENSEARCH_COMPANY_INDEX_ALIAS

    def companies_from_csv(self, file_object):
        """Fetch & cache zipped CSV, and then iterate though contents."""
        with helpers.open_zipped_csv(
            file_object, constants.CH_CSV_FIELDNAMES
        ) as csv_reader:
            next(csv_reader)  # skip the csv header
            for row in csv_reader:
                yield helpers.create_company_document(row)

    def populate_new_index(self):
        client = connections.get_connection()
        with open('company/tests/ch_part1_2.zip', 'rb') as zipped_csv:
            companies = self.companies_from_csv(zipped_csv)
            companies_dicts = (company.to_dict(True) for company in companies)

            bulk(
                client,
                companies_dicts,
                chunk_size=100,
                raise_on_exception=True,
                index=settings.OPENSEARCH_COMPANY_INDEX_ALIAS,
            )

    def refresh_index(self):
        documents.CompanyDocument._index.refresh()

    def handle(self, *args, **options):
        breakpoint()
        self.populate_new_index()
        self.refresh_index()
