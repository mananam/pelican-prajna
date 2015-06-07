# -*- coding: utf-8 -*-
"""Readers for Sloka content."""

from __future__ import unicode_literals, print_function

import json
import logging

from pelican.readers import BaseReader

logger = logging.getLogger(__name__)


class SlokaReader(BaseReader):

    """A reader for sloka content.

    - parse the given file for json content
    - extract metadata, content for the file
    """

    enabled = True
    file_extensions = ['json']
    extensions = None

    def __init__(self, *args, **kwargs):
        """Create an instance of SlokaReader."""
        logger.debug("SlokaReader: Initialize")
        super(SlokaReader, self).__init__(*args, **kwargs)

    def read(self, source_path):
        """Parse the json content in a file.

        Extract metadata and content from a JSON file.

        Returns:
            string, dict: content of the file as string, dictionary of metadata
        """
        logger.debug("SlokaReader: Read: %s", source_path)
        with open(source_path) as f:
            json_content = json.load(f)

        logger.debug("SlokaReader: File content: %s", json_content)
        content = json.dumps(json_content['content'])
        metadata = json_content['metadata']

        return content, metadata
