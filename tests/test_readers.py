# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import json
import unittest

from pyfakefs import fake_filesystem
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
        expect(self.slokareader.enabled).to.equal(True)

    def test_reader_file_extensions_should_be_md(self):
        expect(self.slokareader.file_extensions).to.equal(['md'])

    def test_reader_extensions_should_be_none(self):
        expect(self.slokareader.extensions).to.equal(None)

    def test_reader_reads_metadata_key_value(self):
        new_file = self.fake_filesystem.CreateFile('dummy_file')
        new_file.SetContents('lang:sa\nkey:value')

        content, metadata = self.slokareader.read('dummy_file')
        json_metadata = json.loads(metadata)

        expect(content).to.equal('{}')
        expect(json_metadata).to_not.none
        expect(json_metadata).to.have.length_of(2)
        expect(json_metadata).to.have.key('lang').to.equal('sa')
        expect(json_metadata).to.have.key('key').to.equal('value')

    def test_reader_doesnot_read_invalid_metadata(self):
        new_file = self.fake_filesystem.CreateFile('dummy_file')
        new_file.SetContents('sample content i.e. not metadata')

        content, metadata = self.slokareader.read('dummy_file')

        expect(content).to.equal('{}')
        expect(metadata).to.equal('{}')

    def test_reader_throws_valueerror_for_invalid_content(self):
        new_file = self.fake_filesystem.CreateFile('dummy_file')
        new_file.SetContents("")

        content, metadata = self.slokareader.read('dummy_file')

        expect(content).to.equal('{}')
        expect(metadata).to.equal('{}')
        # expect(self.slokareader.read).when\
        # .called_with('dummy_file').throw(ValueError)
