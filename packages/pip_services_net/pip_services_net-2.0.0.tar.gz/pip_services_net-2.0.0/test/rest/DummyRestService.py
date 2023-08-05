# -*- coding: utf-8 -*-
"""
    test.rest.DummyRestService
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Dummy REST service
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import threading

from pip_services_commons.data import FilterParams, PagingParams, IdGenerator
from pip_services_commons.refer import Descriptor
from pip_services_net.rest import RestService

from ..IDummyService import IDummyService

class DummyRestService(RestService):
    _logic = None

    def __init__(self):
        super(DummyRestService, self).__init__()

    def set_references(self, references):
        # Locate reference to dummy persistence component
        self._logic = references.get_one_required(
            Descriptor("pip-services-dummies", "controller", "*", "*", "*")
        )

        super(DummyRestService, self).set_references(references)

    def get_page_by_filter(self):
        correlation_id = self.get_correlation_id()
        filter = self.get_filter_params()
        paging = self.get_paging_params()
        return self.send_result(self._logic.get_page_by_filter(correlation_id, filter, paging))

    def get_one_by_id(self, id):
        correlation_id = self.get_correlation_id()
        return self.send_result(self._logic.get_one_by_id(correlation_id, id))

    def create(self):
        correlation_id = self.get_correlation_id()
        entity = self.get_data()
        return self.send_created_result(self._logic.create(correlation_id, entity))

    def update(self, id):
        correlation_id = self.get_correlation_id()
        entity = self.get_data()
        return self.send_result(self._logic.update(correlation_id, entity))

    def delete_by_id(self, id):
        correlation_id = self.get_correlation_id()
        self._logic.delete_by_id(correlation_id, id)
        return self.send_deleted_result()

    def handled_error(self):
        raise UnsupportedError('NotSupported', 'Test handled error')

    def unhandled_error(self):
        raise TypeError('Test unhandled error')

    def register(self):
        self.register_route('get', '/dummies', self.get_page_by_filter)
        self.register_route('get', '/dummies/<id>', self.get_one_by_id)
        self.register_route('post', '/dummies', self.create)
        self.register_route('put', '/dummies/<id>', self.update)
        self.register_route('delete', '/dummies/<id>', self.delete_by_id)
        self.register_route('get', '/dummies/handled_error', self.handled_error)
        self.register_route('get', '/dummies/unhandled_error', self.unhandled_error)
