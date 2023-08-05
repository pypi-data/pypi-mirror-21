# -*- coding: utf-8 -*-
"""Test all the resources."""

# python imports
import responses

# local imports
from mls.apiclient import api, resources
from mls.apiclient.tests import base


class IntegrationTestCase(base.BaseTestCase):
    """Test resource class."""

    def setUp(self):
        responses.start()
        self.api = api.API(
            self.BASE_URL,
            api_key='YOUR_API_KEY',
            lang='en',
            debug=True,
        )

    def tearDown(self):
        responses.stop()
        responses.reset()

    def test_development_list(self):
        """Development integration test."""
        self.setup_integration_test()
        developments = resources.Development.search(self.api)
        development_list = developments.get_items()
        self.assertEqual(len(development_list), 25)
