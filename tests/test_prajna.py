# -*- coding: utf-8 -*-

import unittest
import prajna
import pelican.signals

from sure import expect


class PrajnaTests(unittest.TestCase):
    """
    - test_initialized_sets_sloka_settings
    """
    def test_register_should_connect_to_events(self):
        prajna.register()

        expect(pelican.signals.initialized.receivers.keys()).length_of(1)
        expect(pelican.signals.get_generators.receivers.keys()).length_of(1)
        expect(pelican.signals.finalized.receivers.keys()).length_of(1)
        expect(pelican.signals.readers_init.receivers.keys()).length_of(1)
