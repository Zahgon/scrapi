"""
A Lake Winnipeg Basin Information Network (BIN) harvester for the SHARE project

Example API request: http://130.179.67.140/api/3/action/package_search?q= (problematic)
http://130.179.67.140/api/3/action/current_package_list_with_resources (currently using)
It oddly returns 5 more datasets than all searchable ones on LWBIN data hub.

Known issues:
1 -- Five datasets can be searched but cannot be accessed via LWBIN.
Clicking on the searching result would result in linking to a redirected page like this:
http://130.179.67.140/user/login?came_from=http://130.179.67.140/dataset/mpca-surface-water-data-access-interactive-map
Within each dataset there are resouces that contain urls to source pages. For future work considering using resources
urls as canonical urls.
2 -- Resouces properties contained in raw metadata of the datasets are not added to the normalized metadata at this
point.
3 -- Single name contributors can be used as filters or an invalid query will be returned. Has nothing to do with scrapi but the frontend.
"""

from __future__ import unicode_literals

import json
import logging

from dateutil.parser import parse

from scrapi import requests
from scrapi.base import JSONHarvester
from scrapi.linter.document import RawDocument
from scrapi.base.helpers import build_properties, datetime_formatter, parse_name


logger = logging.getLogger(__name__)

ORGANIZATIONS = (
    "organization", "fund", "canada", "agriculture", "commitee", "international", "council", "office", "of",
    "observation", "institute", "lwbin", "cocorahs", "usgs", "nsidc"
)


def is_organization(name):
    """Return a boolean to indicate if the name passed to the function is an organization
    """
    pass


def clean_authors(authors):
    """Cleam authors list.
    """
    pass


def process_contributors(authors, emails):
    """Process authors and add author emails
    If multiple authors and one email, put email in a new author
    """
    pass


def process_licenses(license_title, license_url, license_id):
    """Process licenses to comply with the normalized schema
    """
    pass


def construct_url(url, dataset_path, end_point):
    """
    :return: a url that directs back to the page on LBWIN Data Hub instead of the source page.
    :param url: host url
    :param dataset_path: parent path of all datasets
    :param end_point: name of datasets
    """
    pass


def process_object_uris(url, extras):
    """Extract doi from /extras, and return a list of object uris including /url and doi if it exists.
    """
    pass


class LWBINHarvester(JSONHarvester):
    short_name = 'lwbin'
    long_name = 'Lake Winnipeg Basin Information Network'
    url = 'http://130.179.67.140'
    dataset_path = "dataset"   # dataset base url for constructing urls that go back to LWBIN instead of source pages.

    DEFAULT_ENCODING = 'UTF-8'

    record_encoding = None


    def harvest(self, start_date=None, end_date=None):
        """Returns a list of Rawdocuments (metadata)
        Searching by time is not supported by LWBIN CKAN API. all datasets have to be scanned each time.
        """

        base_url = 'http://130.179.67.140/api/3/action/current_package_list_with_resources'

        records = requests.get(base_url).json()['result']
        total = len(records)  # Total number of documents
        logger.info('{} documents to be harvested'.format(total))

        return [
            RawDocument({
                'doc': json.dumps(record),
                'source': self.short_name,
                'docID': record['id'],
                'filetype': 'json'
            }) for record in records
        ]
