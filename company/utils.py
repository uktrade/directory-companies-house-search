import csv
import io
import zipfile
from contextlib import contextmanager

import requests

from company.doctypes import CompanyDocType

COMPANY_STATUSES = {
    'Active': 'active',
    'Active - Proposal to Strike off': 'active',
    'Dissolved': 'dissolved',
    'Liquidation': 'liquidation',
    'RECEIVER MANAGER / ADMINISTRATIVE RECEIVER': 'liquidation',
    'Receivership': 'receivership',
    'RECEIVERSHIP': 'receivership',
    'Live but Receiver Manager on at least one charge': 'receivership',
    'In Administration': 'administration',
    'ADMINISTRATION ORDER': 'administration',
    'ADMINISTRATIVE RECEIVER': 'administration',
    'In Administration/Administrative Receiver': 'administration',
    'In Administration/Receiver Manager': 'administration',
    'Voluntary Arrangement': 'voluntary-arrangement',
    'VOLUNTARY ARRANGEMENT / ADMINISTRATIVE RECEIVER': 'voluntary-arrangement',
    'VOLUNTARY ARRANGEMENT / RECEIVER MANAGER': 'voluntary-arrangement'
}

LIMITED_COMPANY = 'ltd'
OTHER = 'other'

COMPANY_TYPES = {
    'Private Unlimited Company': 'private-unlimited',
    'Community Interest Company': LIMITED_COMPANY,
    'Private Limited Company': LIMITED_COMPANY,
    'Old Public Company': 'old-public-company',
    'PRI/LBG/NSC (Private, Limited by guarantee, '
    'no share capital, use of \'Limited\' exemption)':
        'private-limited-guarant-nsc-limited-exemption',
    'Limited Partnership': 'limited-partnership',
    'PRI/LTD BY GUAR/NSC (Private, limited by guarantee, no '
    'share capital)': 'private-limited-guarant-nsc',
    'Private Unlimited': 'private-unlimited-nsc',
    'Public Limited Company': 'plc',
    'PRIV LTD SECT. 30 (Private limited company, section 30 of '
    'the Companies Act)':
        'private-limited-shares-section-30-exemption',
    'Investment Company with Variable Capital(Umbrella)': 'icvc-umbrella',
    'Industrial and Provident Society': 'industrial-and-provident-society',
    'Northern Ireland': 'northern-ireland',
    'Limited Liability Partnership': 'llp',
    'Royal Charter Company': 'royal-charter',
    'Investment Company with Variable Capital':
        'investment-company-with-variable-capital',
    'Unregistered Company': 'unregistered-company',
    'Registered Society': 'registered-society-non-jurisdictional',
    'Other Company Type': OTHER,
    'Other company type': OTHER,
    'European Public Limited-Liability Company (SE)':
        'european-public-limited-liability-company-se',
    'Scottish Partnership': 'scottish-partnership',
    'Charitable Incorporated Organisation':
        'charitable-incorporated-organisation',
    'Scottish Charitable Incorporated Organisation':
        'scottish-charitable-incorporated-organisation',
    'Protected Cell Company': 'protected-cell-company',
    'Investment Company with Variable Capital (Securities)': 'icvc-securities',
}


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
    row_formatter = RowFormatter(row)
    company = {
        'company_name': row['CompanyName'],
        'company_number': row['CompanyNumber'],
        'company_status': COMPANY_STATUSES.get(
            row['CompanyStatus'], row['CompanyStatus']
        ),
        'type': COMPANY_TYPES.get(
            row['CompanyCategory'], row['CompanyCategory']),
        'date_of_cessation': row['DissolutionDate'],
        'date_of_creation': row['IncorporationDate'],
        'country_of_origin': row['CountryOfOrigin'],
        'sic_codes': row_formatter.sic_codes,
        'address_snippet': row_formatter.address_snippet,
        'address': row_formatter.address,
    }
    return CompanyDocType(
        meta={'id': company['company_number']},
        **company
    )


class RowFormatter:

    def __init__(self, row):
        self.row = row

    @property
    def sic_codes(self):
        codes = []
        filtered_codes = self.filter_empty(
            self.row['SICCode.SicText_1'],
            self.row['SICCode.SicText_2'],
            self.row['SICCode.SicText_3'],
            self.row['SICCode.SicText_4'],
        )
        for sic_code in filtered_codes:
            try:
                codes.append(sic_code.split(' - ')[0])
            except IndexError:
                pass
        return codes

    @property
    def address(self):
        return {
            'care_of': self.row['RegAddress.CareOf'],
            'po_box': self.row['RegAddress.POBox'],
            'address_line_1': self.row['RegAddress.AddressLine1'],
            'address_line_2': self.row['RegAddress.AddressLine2'],
            'locality': self.row['RegAddress.PostTown'],
            'region': self.row['RegAddress.County'],
            'country': self.row['RegAddress.Country'],
            'postal_code': self.row['RegAddress.PostCode']
        }

    @property
    def address_snippet(self):
        filtered_address = self.filter_empty(
            self.address['address_line_1'],
            self.address['address_line_2'],
            self.address['locality'],
            self.address['region'],
            self.address['country'],
            self.address['postal_code']
        )
        return ', '.join(filtered_address)

    @staticmethod
    def filter_empty(*values):
        return filter(lambda x: x != '', values)
