import json
import copy

import jsonschema

from scrapi import registry
from scrapi.util import json_without_bytes


def strip_empty(document, required=tuple()):
    ''' Removes empty fields from the processed schema
    '''
    pass




def do_strip_empty(value):
    ''' Filters empty values from container types
    '''
    pass


class BaseDocument(object):

    """
        For file objects. Automatically validates input to ensure
        compatibility with scrAPI.
    """

    schema = {}
    format_checker = jsonschema.FormatChecker()

    def __init__(self, attributes, validate=True, clean=False):
        ''' Initializes a document

            :param dict attributes: the dictionary representation of a document
            :param bool validate: If true, the object will be validated before creation
            :param bool clean: If true, optional fields that are null will be deleted
        '''
        attributes = attributes or {}
        # validate a version of the attributes that are safe to check
        # against the JSON schema

        # Allows validation in python3
        self.attributes = json_without_bytes(copy.deepcopy(attributes))
        if clean:
            self.attributes = strip_empty(self.attributes, required=self.schema.get('required', []))
        if validate:
            self.validate()


    def get(self, attribute, default=None):
        """
            Maintains compatibility with previous dictionary implementation of scrAPI
            :: str -> str
        """
        return self.attributes.get(attribute, default)

    def __getitem__(self, attr):
        return self.attributes[attr]

    def __setitem__(self, attr, val):
        self.attributes[attr] = val

    def __delitem__(self, attr):
        del self.attributes[attr]

    def __bool__(self):
        return bool(self.attributes)

    __nonzero__ = __bool__


class RawDocument(BaseDocument):


    def __repr__(self):
        return "RawDocument(source='{source}', docID='{docID}', filetype='{filetype}', ...)".format(
            source=self.attributes.get('source'),
            docID=self.attributes.get('docID'),
            filetype=self.attributes.get('filetype')
        )


class NormalizedDocument(BaseDocument):

    with open('normalized.json') as f:
        schema = json.load(f)

    def __repr__(self):
        return "NormalizedDocument(source='{}', url='{}', providerUpdatedDateTime='{}', ...)".format(
            self.attributes.get('shareProperties', {}).get('source'),
            self.attributes.get('uris', {}).get('canonicalUri'),
            self.attributes.get('providerUpdatedDateTime')
        )
