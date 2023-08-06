# -*- coding: utf-8 -*-
"""
    test.memory.DummyMemoryPersistence
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Dummy memory persistence implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services_commons.data import FilterParams
from pip_services_data.memory import IdentifiableMemoryPersistence
from ..IDummyPersistence import IDummyPersistence

class DummyMemoryPersistence(IdentifiableMemoryPersistence, IDummyPersistence):
    
    def __init__(self):
        super(DummyMemoryPersistence, self).__init__()

    def get_page_by_filter(self, correlation_id, filter, paging):
        filter = filter if filter != None else FilterParams()
        key = filter.get_as_nullable_string("key")

        def filter_dummy(obj):
            if key != None and obj['key'] != key:
                return False
            return True
            
        return super(DummyMemoryPersistence, self).get_page_by_filter(correlation_id, filter_dummy, paging)
