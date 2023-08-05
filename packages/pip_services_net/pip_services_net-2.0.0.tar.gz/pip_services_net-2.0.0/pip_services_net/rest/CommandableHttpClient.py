# -*- coding: utf-8 -*-
"""
    pip_services_commons.rest.CommandableHttpClient
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Commandable HTTP client implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .RestClient import RestClient

class CommandableHttpClient(RestClient):
    _name = None

    def __init__(self, name):
        super(CommandableHttpClient, self).__init__()
        self._name = name


    def call_command(self, name, correlation_id, params):
        timing = self._instrument(correlation_id, self._name + '.' + name)
        try:
            route = '/'  + self._name + '/' + name
            return self.call('POST', route, correlation_id, None, params)
        finally:
            timing.end_timing()