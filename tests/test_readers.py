# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import unittest

import fake_filesystem
import sure

from unittest.mock import patch
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

        filesystem = fake_filesystem.FakeFilesystem()
        os_module = fake_filesystem.FakeOsModule(filesystem)

        patcher = patch('os.path', os_module.path)
        patcher.start()
        self.addCleanup(patcher.stop)


    def test_reader_enabled_by_default(self):
        self.slokareader.enabled.should.be.equal(True)


    def test_reader_file_extensions_should_be_json(self):
        self.slokareader.file_extensions.should.equal(['json'])


    def test_reader_extensions_should_be_none(self):
        self.slokareader.extensions.should.be.equal(None)

    def test_reader_read_should_only_read_json_files(self):
        dummy_file = "/some/file.txt"

        content, metadata = self.slokareader.read(dummy_file)

        content.should.be.equal(None)
        metadata.should.be.equal(None)
