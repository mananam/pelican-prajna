# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import unittest

import sure

from prajna.readers import SlokaReader

class SlokaReaderTests(unittest.TestCase):
    """
    - test default metadata
    - test valid json
    -
    - test invalid json
    - test custom validation rule
    """
    def setUp(self):
        settings = None
        self.slokareader = SlokaReader(settings)


    def test_reader_enabled_by_default(self):
        self.slokareader.enabled.should.be.equal(True)


    def test_reader_file_extensions_should_be_json(self):
        self.slokareader.file_extensions.should.equal(['json'])


    def test_reader_extensions_should_be_none(self):
        self.slokareader.extensions.should.be.equal(None)
