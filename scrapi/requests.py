"""A wrapper around requests that records all requests made with it.
    Supports get, put, post, delete and request
    all calls return an instance of HarvesterResponse
"""
from __future__ import absolute_import

import json
import time
import logging
import functools

import six
import furl
import requests

from scrapi import events
from scrapi import settings
from scrapi.processing import HarvesterResponse


logger = logging.getLogger(__name__)








def request(method, url, params=None, **kwargs):
    """Make a recorded request or get a record matching method and url

    :param str method: Get, Put, Post, or Delete
    :param str url: Where to make the request to
    :param bool force: Whether or not to force the new request to be made
    :param int throttle: A time in seconds to sleep before making requests
    :param dict kwargs: Addition keywords to pass to requests
    """
    pass


get = functools.partial(request, 'get')
put = functools.partial(request, 'put')
post = functools.partial(request, 'post')
delete = functools.partial(request, 'delete')
