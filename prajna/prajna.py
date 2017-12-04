# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from pelican import signals

import os

#initialized = signal('pelican_initialized')
#get_generators = signal('get_generators')
#finalized = signal('pelican_finalized')

# Reader-level signals

#readers_init = signal('readers_init')

# Generator-level signals

#generator_init = signal('generator_init')

#article_generator_init = signal('article_generator_init')
#article_generator_finalized = signal('article_generator_finalized')

#page_generator_init = signal('page_generator_init')
#page_generator_finalized = signal('page_generator_finalized')

#static_generator_init = signal('static_generator_init')
#static_generator_finalized = signal('static_generator_finalized')

# Page-level signals

#article_generator_preread = signal('article_generator_preread')
#article_generator_context = signal('article_generator_context')

#page_generator_preread = signal('page_generator_preread')
#page_generator_context = signal('page_generator_context')

#static_generator_preread = signal('static_generator_preread')
#static_generator_context = signal('static_generator_context')

#content_object_init = signal('content_object_init')

## Writers signals
#content_written = signal('content_written')


def on_initialized(pelican_object):
    # add a generator pelican_object.get_generator_classes()
    pelican_object.settings['SLOKA_DIR'] = ""
    pelican_object.settings['SLOKA_EXCLUDES'] = ""

    # settings used by writers
    pelican_object.settings['SLOKA_URL'] = "{slug}/index.html"
    pelican_object.settings['SLOKA_SAVE_AS'] = "{slug}/index.html"

    # TODO respect user's themes?
    pelican_object.settings['THEME'] = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '../theme')
    pelican_object.theme = pelican_object.settings['THEME']

    # TODO remove default templates
    pelican_object.settings['DIRECT_TEMPLATES'] = []
    pelican_object.settings['PAGINATED_DIRECT_TEMPLATES'] = []

    # metadata
    pelican_object.settings['SLOKA_LANG_SAVE_AS'] = "{slug}/index.html"
    pelican_object.settings['SLOKA_LANG_URL'] = "{lang}/{slug}/index.html"


def on_readers_init(readers):
    # add reader
    from .readers import SlokaReader
    readers.reader_classes['md'] = SlokaReader


def on_get_generators(pelican_object):
    # return the generators in this class
    from .generators import SlokaGenerator
    return [SlokaGenerator]


def on_connect(*args, **kwargs):
    pass
