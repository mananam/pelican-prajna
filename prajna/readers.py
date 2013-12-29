# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

from pelican.readers import BaseReader

class SlokaReader(BaseReader):
    enabled = True
    file_extensions = ['json']
    extensions = None

    def __init__(self, *args, **kwargs):
        print("reader: init")
        super(SlokaReader, self).__init__(*args, **kwargs)

    def read(self, source_path):
        #import pudb
        #pudb.set_trace()
        print("SlokaReader read: ", self, source_path)
        content = 'some content'
        metadata = {'text': 'something'}
        return content, metadata
