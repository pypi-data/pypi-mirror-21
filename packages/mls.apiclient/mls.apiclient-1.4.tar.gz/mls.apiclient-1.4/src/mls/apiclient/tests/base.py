# -*- coding: utf-8 -*-
"""Test case base class."""

# python imports
try:
    import unittest2 as unittest
except ImportError:
    import unittest

# local imports
from mls.apiclient import (
    REST_API_URL,
    REST_API_VERSION,
    testing,
)
from mls.apiclient.utils import join_url


class BaseTestCase(unittest.TestCase):
    """Test case base class."""
    HOST = 'demomls.com'
    PATH = '/api'

    @property
    def BASE_URL(self):
        """Return the MLS base url used for the tests."""
        return 'http://{0}'.format(self.HOST)

    @property
    def URL(self):
        """Return the MLS API endpoint url for the tests."""
        return self.BASE_URL + self.PATH

    @property
    def API_BASE(self):
        """Return the base API url for the tests."""
        return join_url(self.BASE_URL, REST_API_URL, REST_API_VERSION)

    def setup_integration_test(self):
        """Setup all URL mocks to run a full integration test."""

        testing.setup_fixtures()

        base_params = {
            'apikey': 'YOUR_API_KEY',
            'lang': 'en',
        }

        # register all the field endpoints
        testing._register(
            'field_titles/developments',
            params=base_params,
            fixture='development_fields_en.json',
        )
        testing._register(
            'field_order/developments',
            params=base_params,
            fixture='development_fields_order.json',
        )
        testing._register(
            'field_titles/development_groups',
            params=base_params,
            fixture='group_fields_en.json',
        )
        testing._register(
            'field_order/development_groups',
            params=base_params,
            fixture='group_fields_order.json',
        )
        testing._register(
            'field_titles/development_phases',
            params=base_params,
            fixture='phase_fields_en.json',
        )
        testing._register(
            'field_order/development_phases',
            params=base_params,
            fixture='phase_fields_order.json',
        )

        # register the development endpoints
        testing._register(
            'developments',
            params=base_params,
            fixture='integration/development_list_26-1.json',
        )
        testing._register(
            'developments',
            params=dict({'limit': 25, 'offset': 25, }, **base_params),
            fixture='integration/development_list_26-2.json',
        )
        testing._register(
            'developments',
            params=dict({'agency_developments': 'dev-agency'}, **base_params),
            fixture='integration/development_list_15-agency1.json',
        )
        testing._register(
            'developments',
            params=dict({'agency_developments': 'budget-dev'}, **base_params),
            fixture='integration/development_list_11-agency2.json',
        )
