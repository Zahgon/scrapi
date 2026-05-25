'''
Harvester for the MAXWELL for the SHARE project

Example API call: http://www.maxwell.vrac.puc-rio.br/DC_Todos.php?verb=ListRecords&metadataPrefix=oai_dc
'''
from __future__ import unicode_literals

from scrapi.base import OAIHarvester
from scrapi.base import helpers




class PcurioHarvester(OAIHarvester):
    short_name = 'pcurio'
    long_name = 'Pontifical Catholic University of Rio de Janeiro'
    url = 'http://www.maxwell.vrac.puc-rio.br'


    base_url = 'http://www.maxwell.vrac.puc-rio.br/DC_Todos.php'
    property_list = ['date', 'identifier', 'type', 'setSpec']
    timezone_granularity = False
