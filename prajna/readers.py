# -*- coding: utf-8 -*-
"""Readers for Sloka content."""

from __future__ import unicode_literals, print_function

import json
import logging

from pelican.readers import BaseReader

logger = logging.getLogger(__name__)


class SlokaReader(BaseReader):
    """A commonmarkdown based reader for sanskrit verses.

    Uses following additional markup to extract special context:

        <!-- Verse Metadata -->
        Key: Value

        <!-- Verse -->
        ~~~sloka
        line1
        line2
        line3
        ~~~

        ~~~padachhed
        word1 word2
        word2a word2b
        word3a
        ~~~

        ~~~anvaya
        word2a word1 word3a word2 word2b
        ~~~

    TODO sloka, padachhed, anvaya are styled differently.
    """

    enabled = True
    file_extensions = ['md']
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

        import CommonMark
        metadata = {}
        content = {}
        with open(source_path) as f:
            # parse the metadata
            line = f.readline().rstrip().split(":", 1)
            while len(line) == 2:
                metadata[line[0]] = line[1]
                line = f.readline().rstrip().split(":", 1)

            parser = CommonMark.Parser()
            ast = parser.parse(f.read())
            walker = ast.walker()
            event = walker.nxt()
            while event is not None:
                node = event["node"]
                if node.t == "CodeBlock":
                    content[node.info] = node.literal.rstrip()
                event = walker.nxt()
        json_content = json.dumps(content)
        return json_content, json.dumps(metadata)

    def _is_valid_node(self, node):
        pass
