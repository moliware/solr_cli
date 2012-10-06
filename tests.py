# -*- coding: utf-8 -*-

import unittest
from solr_cli import SolrCLI


class SolrCLITestCase(unittest.TestCase):

    def setUp(self):
        self.cli = SolrCLI()

    def tearDown(self):
        pass

    def test_connect(self):
        self.cli.do_connect('http://localhost:8983/solr')
        self.assertTrue(self.cli.connected)