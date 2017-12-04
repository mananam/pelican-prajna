# -*- coding: utf-8 -*-

import unittest
import unittest.mock
import prajna
import prajna.readers
import prajna.generators
import pelican.signals

from sure import expect


class PrajnaTests(unittest.TestCase):
    """
    Tests for the pelican hooks in prajna.
    """
    def test_register_should_connect_to_events(self):
        prajna.register()

        expect(pelican.signals.initialized.receivers.keys()).length_of(1)
        expect(pelican.signals.get_generators.receivers.keys()).length_of(1)
        expect(pelican.signals.finalized.receivers.keys()).length_of(1)
        expect(pelican.signals.readers_init.receivers.keys()).length_of(1)

    def test_on_initialized_should_set_prajna_settings(self):
        s = {}
        pelican_object = unittest.mock.MagicMock()
        pelican_object.settings.__setitem__.side_effect = s.__setitem__

        prajna.prajna.on_initialized(pelican_object)

        expect(s['SLOKA_DIR']).length_of(0)
        expect(s['SLOKA_EXCLUDES']).length_of(0)
        expect(s['SLOKA_URL']).to.equal("{slug}/index.html")
        expect(s['SLOKA_SAVE_AS']).to.equal("{slug}/index.html")
        expect(s['SLOKA_LANG_URL']).to.equal("{lang}/{slug}/index.html")
        expect(s['SLOKA_LANG_SAVE_AS']).to.equal("{slug}/index.html")
        expect(s['DIRECT_TEMPLATES']).length_of(0)
        expect(s['PAGINATED_DIRECT_TEMPLATES']).length_of(0)

    def test_on_initialized_should_set_prajna_theme(self):
        s = {}
        pelican_object = unittest.mock.MagicMock()
        pelican_object.settings.__setitem__.side_effect = s.__setitem__
        p = unittest.mock.PropertyMock()
        type(pelican_object).theme = p

        prajna.prajna.on_initialized(pelican_object)

        expect(s['THEME']).to.contain("theme")
        p.assert_called_once()

    def test_on_readers_init_should_set_slokareader(self):
        s = {}
        readers = unittest.mock.MagicMock()
        readers.reader_classes.__setitem__.side_effect = s.__setitem__

        prajna.prajna.on_readers_init(readers)

        expect(s['md']).to.be(prajna.readers.SlokaReader)

    def test_on_get_generators_should_set_slokagenerator(self):
        pelican_object = unittest.mock.MagicMock()

        gen = prajna.prajna.on_get_generators(pelican_object)

        expect(gen).to.eql([prajna.generators.SlokaGenerator])

    def test_on_connect_should_not_throw(self):
        expect(prajna.prajna.on_connect).to_not.throw()
