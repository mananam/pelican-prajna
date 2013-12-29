# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from pelican import signals

from prajna import prajna

def register():
    signals.initialized.connect(prajna.on_initialized)
    signals.get_generators.connect(prajna.on_get_generators)
    signals.finalized.connect(prajna.on_connect)
    signals.readers_init.connect(prajna.on_readers_init)
    #signals.generator_init.connect(on_connect)
    #signals.article_generator_init.connect(on_connect)
    #signals.article_generator_finalized.connect(on_connect)
    #signals.page_generator_init.connect(on_connect)
    #signals.page_generator_finalized.connect(on_connect)
    #signals.static_generator_init.connect(on_connect)
    #signals.static_generator_finalized.connect(on_connect)
    #signals.article_generator_preread.connect(on_connect)
    #signals.article_generator_context.connect(on_connect)
    #signals.page_generator_preread.connect(on_connect)
    #signals.page_generator_context.connect(on_connect)
    #signals.static_generator_preread.connect(on_connect)
    #signals.static_generator_context.connect(on_connect)
    #signals.content_object_init.connect(on_connect)
    #signals.content_written.connect(on_connect)
