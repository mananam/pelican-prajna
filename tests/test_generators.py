# -*- coding: utf-8 -*-
import unittest
import unittest.mock
import prajna.generators

from sure import expect


class SlokaTests(unittest.TestCase):
    def test_sloka_converts_markdown_to_html(self):
        c = {'PATH': "/tmp"}
        content = '{"sloka": "s", "padachhed": "p", "anvaya": "a"}'
        context = unittest.mock.MagicMock()
        context.__getitem__.side_effect = c.__getitem__

        sloka = prajna.generators.Sloka(content,
                                        source_path="/tmp/ch1/01.md",
                                        context=context)

        # TODO assert html content
        expect(sloka.text).to.eql(content)


class SlokaGeneratorTests(unittest.TestCase):
    """
    Tests for sloka generators.
    - test_generate_context_settings
    """
