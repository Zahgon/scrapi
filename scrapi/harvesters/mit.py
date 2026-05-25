"""Harvests MIT DSpace metadata for ingestion into the SHARE service

More information available here:
https://github.com/CenterForOpenScience/SHARE/blob/master/providers/edu.mit.md

Example metadata URL: http://dspace.mit.edu/oai/request?verb=ListRecords&metadataPrefix=oai_dc&from=2014-09-28
"""


from __future__ import unicode_literals

from scrapi.base import OAIHarvester


class MITHarvester(OAIHarvester):
    short_name = 'mit'
    long_name = 'DSpace@MIT'
    url = 'http://dspace.mit.edu/'

    base_url = 'http://dspace.mit.edu/oai/request'
    property_list = [
        'type', 'source', 'format', 'rights', 'identifier',
        'relation', 'date', 'description', 'setSpec'
    ]

