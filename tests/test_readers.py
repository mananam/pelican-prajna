# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import unittest

import fake_filesystem
from sure import expect

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

        self.fake_filesystem = fake_filesystem.FakeFilesystem()
        self.fake_os_module = fake_filesystem\
            .FakeOsModule(self.fake_filesystem)
        self.fake_file_open = fake_filesystem\
            .FakeFileOpen(self.fake_filesystem)

        patcher = patch('builtins.open', self.fake_file_open)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_reader_enabled_by_default(self):
        expect(self.slokareader.enabled).to.be(True)

    def test_reader_file_extensions_should_be_json(self):
        expect(self.slokareader.file_extensions).to.equal(['json'])

    def test_reader_extensions_should_be_none(self):
        expect(self.slokareader.extensions).to.equal(None)

    def test_reader_reads_metadata_from_json_file(self):
        new_file = self.fake_filesystem.CreateFile('dummy_file')
        new_file.SetContents('{"metadata":"", "content":""}')

        content, metadata = self.slokareader.read('dummy_file')

        expect(content).to.equal('""')
        expect(metadata).be.empty

    def test_reader_throws_valueerror_for_invalid_content(self):
        new_file = self.fake_filesystem.CreateFile('dummy_file')
        new_file.SetContents("dummy_contents")

        expect(self.slokareader.read).when\
            .called_with('dummy_file').throw(ValueError)
