# -*- coding: utf-8 -*-
import os.path
import unittest
import unittest.mock

from prajna.generators import Sloka, SlokaGenerator

import pelican.settings
from pelican.writers import Writer

from pyfakefs import fake_filesystem
from sure import expect


class SlokaTests(unittest.TestCase):
    def test_sloka_converts_markdown_to_html(self):
        c = {'PATH': "/tmp"}
        content = '{"sloka": "s", "padachhed": "p", "anvaya": "a"}'
        context = unittest.mock.MagicMock()
        context.__getitem__.side_effect = c.__getitem__

        sloka = Sloka(content,
                      source_path="/tmp/ch1/01.md",
                      context=context)

        expect(sloka.text).to.eql(content)
        expect(sloka.sloka).to.eql("<p>s</p>\n")
        expect(sloka.padachhed).to.eql("p")
        expect(sloka.anvaya).to.eql("a")

        expect(sloka.slug).to.eql("ch1.01.md")


class SlokaGeneratorTests(unittest.TestCase):
    """
    Tests for sloka generators.
    - test_generate_context_self.settings
    """
    def setUp(self):
        self.path = "/tmp/prajna_test"
        self.context = {'PATH': os.path.join(self.path, "01.md")}
        self.settings = pelican.settings.DEFAULT_CONFIG
        self.theme = "/tmp/prajna_test/theme"
        outpath = "output/test.html"

        self.settings['PATH'] = self.path
        # use self.path as input dir
        self.settings['SLOKA_DIR'] = "input/"
        self.settings['SLOKA_EXCLUDES'] = []
        self.settings['SLOKA_SAVE_AS'] = os.path.join(self.path, "01.html")
        self.settings['WRITE_SELECTED'] = []
        self.slokagen = SlokaGenerator(context=self.context,
                                       settings=self.settings,
                                       path=self.path,
                                       theme=self.theme,
                                       output_path=outpath)

        self.fake_filesystem = fake_filesystem.FakeFilesystem()
        self.fake_os_module = fake_filesystem\
            .FakeOsModule(self.fake_filesystem)
        self.fake_file_open = fake_filesystem\
            .FakeFileOpen(self.fake_filesystem)

        self._create_patch('builtins.open', self.fake_file_open)
        self._create_patch('os.stat', self.fake_os_module.stat)
        self._create_patch('os.walk', self.fake_os_module.walk)

    def test_generate_output_should_write_html_file(self):
        writer = Writer("/tmp/out.html", settings=self.settings)
        self._create_fake_files()
        self.slokagen.articles = [self._get_sloka()]

        self.slokagen.generate_output(writer)

        with open(os.path.join(self.path, "01.html"), 'r') as f:
            expect(f.readline()).to.eql("<p>s</p>\n")

    def test_generate_context_should_read_files(self):
        self._create_fake_files()

        self.slokagen.generate_context()

        expect(self.slokagen.articles).to.length_of(1)
        expect(self.slokagen.articles[0].sloka).to.eql("<p>s</p>\n")
        expect(self.slokagen.articles[0].padachhed).to.eql("p")
        expect(self.slokagen.articles[0].anvaya).to.eql("a")

    def test_generate_context_should_skip_info_files(self):
        # TODO support index files
        self._create_fake_files()
        self._create_input_file("info.json", "{}")

        self.slokagen.generate_context()

        # info.json should be skipped
        expect(self.slokagen.articles).to.length_of(1)
        expect(self.slokagen.articles[0].sloka).to.eql("<p>s</p>\n")

    def _create_fake_files(self):
        self.fake_os_module.makedirs(self.path, exist_ok=True)

        # Create a theme directory
        template_dir = os.path.join(self.theme, "templates")
        template_file = os.path.join(template_dir, "sloka.html")
        self.fake_os_module.makedirs(template_dir, exist_ok=True)
        with open(template_file, 'w') as f:
            f.write("{{ sloka.sloka }}")

        # Create a fake input file
        content = "~~~sloka\ns\n~~~\n~~~padachhed\np\n~~~\n~~~anvaya\na\n~~~"
        self._create_input_file("01.md", content)

    def _create_input_file(self, name, content):
        input_dir = os.path.join(self.path, self.settings['SLOKA_DIR'])
        input_file = os.path.join(input_dir, name)
        self.fake_os_module.makedirs(input_dir, exist_ok=True)
        f = self.fake_filesystem.CreateFile(input_file)
        f.SetContents(content)

    def _create_patch(self, method, patch):
        patcher = unittest.mock.patch(method, patch)
        patcher.start()
        self.addCleanup(patcher.stop)

    def _get_sloka(self):
        content = '{"sloka": "s", "padachhed": "p", "anvaya": "a"}'
        sloka = Sloka(content,
                      source_path="/tmp/ch1/01.md",
                      context=self.context)
        return sloka
