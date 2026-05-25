'''
Harvester for the DataCite MDS for the SHARE project

Example API call: http://oai.datacite.org/oai?verb=ListRecords&metadataPrefix=oai_dc
'''
from __future__ import unicode_literals

from scrapi.base import OAIHarvester
from scrapi.base.helpers import updated_schema, oai_extract_dois, compose, single_result


class DataciteHarvester(OAIHarvester):
    short_name = 'datacite'
    long_name = 'DataCite MDS'
    url = 'http://oai.datacite.org/'

    base_url = 'http://oai.datacite.org/oai'
    property_list = ['date', 'identifier', 'setSpec', 'description']
    timezone_granularity = True



def get_second_description(descriptions):
    ''' In the DataCite OAI PMH api, there are often 2 descriptions: A type and
    a longer kind of abstract. If there are two options, pick the second one which
    is almost always the longer abstract
    '''
    pass
