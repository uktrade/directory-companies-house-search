import csv
import io
import zipfile
from contextlib import contextmanager

import requests

from company.doctypes import CompanyDocType


@contextmanager
def open_zipped_csv(file_pointer, fieldnames):
    """
    Enclose all the complicated logic of on-the-fly unzip->csv read in a
    nice context manager.
    """
    with zipfile.ZipFile(file_pointer) as zip_file:
        # get the first file from zip, assuming it's the only one
        csv_name = zip_file.filelist[0].filename
        with zip_file.open(csv_name) as raw_csv_file_pointer:
            # We need to read that as a text IO for CSV reader to work
            csv_fp = io.TextIOWrapper(raw_csv_file_pointer)

            yield csv.DictReader(csv_fp, fieldnames=fieldnames)


def stream_to_file_pointer(url, file_pointer):
    """Efficiently stream given url to given file pointer."""
    response = requests.get(url, stream=True)
    chuck_size = 4096
    for chunk in response.iter_content(chunk_size=chuck_size):
        file_pointer.write(chunk)


def create_company_document(row):
    address = {
        'care_of': row['RegAddress.CareOf'],
        'po_box': row['RegAddress.POBox'],
        'address_line_1': row['RegAddress.AddressLine1'],
        'address_line_2': row['RegAddress.AddressLine2'],
        'locality': row['RegAddress.PostTown'],
        'region': row['RegAddress.County'],
        'country': row['RegAddress.Country'],
        'postal_code': row['RegAddress.PostCode']
    }
    address_snippet_elements = filter(
        lambda x: x != '',
        (
            address['address_line_1'],
            address['address_line_2'],
            address['locality'],
            address['region'],
            address['country'],
            address['postal_code']
        )
    )
    address_snippet = ', '.join(address_snippet_elements)
    company = {
        'company_name': row['CompanyName'],
        'company_number': row['CompanyNumber'],
        'company_status': row['CompanyStatus'],
        'company_type': row['CompanyCategory'],
        'date_of_cessation': row['DissolutionDate'],
        'date_of_creation': row['IncorporationDate'],
        'country_of_origin': row['CountryOfOrigin'],
        'address_snippet': address_snippet,
        'address': address
    }
    return CompanyDocType(
        meta={'id': company['company_number']},
        **company
    )
