# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import json
import logging

from pelican.readers import BaseReader

logger = logging.getLogger(__name__)


class SlokaReader(BaseReader):
    enabled = True
    file_extensions = ['json']
    extensions = None

    def __init__(self, *args, **kwargs):
        logger.debug("SlokaReader: Initialize")
        super(SlokaReader, self).__init__(*args, **kwargs)

    def read(self, source_path):
        logger.debug("SlokaReader: Read: %s", source_path)
        with open(source_path) as f:
            json_content = json.load(f)

        logger.debug("SlokaReader: File content: %s", json_content)
        content = json_content['content']
        metadata = json_content['metadata']
        return content, metadata
