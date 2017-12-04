# -*- coding: utf-8 -*-

import pelican.signals

from prajna import prajna


def register():
    """Register handlers for pelican signals."""
    pelican.signals.initialized.connect(prajna.on_initialized)
    pelican.signals.get_generators.connect(prajna.on_get_generators)
    pelican.signals.finalized.connect(prajna.on_connect)
    pelican.signals.readers_init.connect(prajna.on_readers_init)
