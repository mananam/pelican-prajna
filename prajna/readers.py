# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import logging
import os

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
        source_file_ext = os.path.splitext(source_path)[-1][1:]
        if (source_file_ext not in self.file_extensions):
            logger.debug("SlokaReader: Read: Skip %s", source_path)
            return None, None

        content = 'some content'
        metadata = {'text': 'something'}
        return content, metadata
