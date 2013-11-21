# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

from unittest import TestCase

import sure

from prajna.readers import SlokaReader

class SlokaReaderTests(TestCase):
    """
    - test default metadata
    - test valid json
    -
    - test invalid json
    - test custom validation rule
    """
    def test_reader_enabled_by_default(self):
        settings = None

        slokareader = SlokaReader(settings)

        slokareader.enabled.should.be.equal(True)


    def test_reader_file_extensions_should_be_json(self):
        pass
