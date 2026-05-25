'''
Harvester for the WHOAS at MBLWHOI Library for the SHARE project

Example API call: http://darchive.mblwhoilibrary.org/oai/request?verb=ListRecords&metadataPrefix=oai_dc
'''
from __future__ import unicode_literals

from scrapi.base import helpers
from scrapi.base import OAIHarvester


class MblwhoilibraryHarvester(OAIHarvester):
    short_name = 'mblwhoilibrary'
    long_name = 'WHOAS at MBLWHOI Library'
    url = 'http://darchive.mblwhoilibrary.org'


    base_url = 'http://darchive.mblwhoilibrary.org/oai/request'
    property_list = ['date', 'relation', 'identifier', 'type', 'format', 'setSpec']
    timezone_granularity = True
