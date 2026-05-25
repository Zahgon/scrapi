"""Harvests Biodiversity Heritage Library OAI Repository (BHL) metadata for ingestion into the SHARE service.
Example API call: http://www.biodiversitylibrary.org/oai?verb=ListRecords&metadataPrefix=oai_dc&from=2015-02-01
"""
import re
from scrapi.base import OAIHarvester
from scrapi.base.helpers import updated_schema, default_name_parser


def institution_name_parser(names):
    ''' Parse institution names '''
    pass


def process_contributors(*args):
    ''' Parse people name for BHL'''
    pass


class BHLHarvester(OAIHarvester):
    short_name = 'bhl'
    long_name = 'Biodiversity Heritage Library OAI Repository'
    url = 'http://www.biodiversitylibrary.org/'

    base_url = 'http://www.biodiversitylibrary.org/oai'


    property_list = [
        'type', 'date', 'relation', 'setSpec', 'rights'
    ]
