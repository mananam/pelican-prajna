# -*- coding: utf-8 -*-
"""A generator for prajna."""

from __future__ import unicode_literals, print_function

import logging
import json
import os.path

from pelican.generators import Generator
from pelican.contents import Content, is_valid_content

logger = logging.getLogger(__name__)


class Sloka(Content):
    """Represents a single sloka."""

    mandatory_properties = ('text',)
    default_template = 'sloka'

    def __init__(self, content, metadata=None, settings=None,
                 source_path=None, context=None):
        """Create an instance of Sloka content."""
        # content is json, parse it
        self.text = content
        json_content = json.loads(content)
        # TODO handle \n to <br/> conversion
        self.sloka = self._markdown_to_html(json_content["sloka"])
        self.padachhed = json_content["padachhed"]
        self.anvaya = json_content["anvaya"]

        # create a slug based on path from PATH directory
        # TODO override slug always to this format:
        # chapter.section.sloka
        child_path = source_path[len(context['PATH'])+1:]
        self.slug = os.path.splitext(child_path)[0].replace(os.path.sep, '.')
        self.slug += os.path.splitext(child_path)[1]

        super(Sloka, self).__init__(content, metadata, settings, source_path,
                                    context)

    def _markdown_to_html(self, mdtext):
        """Convert markdown content to html for render."""
        from CommonMark.render.html import HtmlRenderer
        from CommonMark.cmark import CommonMark
        parser = CommonMark.Parser()
        ast = parser.parse(mdtext)
        renderer = HtmlRenderer()
        renderer.softbreak = "<br/>"
        return renderer.render(ast)


class SlokaGenerator(Generator):
    """Generate pages.

    - traverse thru all files
    - generate_context: call the reader to parse and return html content
    - generate_output: call the writers to write html output
    """

    def __init__(self, *args, **kwargs):
        """Create an instance of SlokaGenerator."""
        super(SlokaGenerator, self).__init__(*args, **kwargs)

    def generate_context(self):
        """Add the articles into the shared context."""
        logger.debug("SlokaGenerator: Generate context")

        self.articles = []
        for f in self.get_files(
                self.settings['SLOKA_DIR'],
                exclude=self.settings['SLOKA_EXCLUDES']):
            try:
                # TODO index files
                if f.endswith("info.json"):
                    continue

                sloka = self.readers.read_file(
                    base_path=self.path, path=f, content_class=Sloka,
                    context=self.context,
                    preread_signal=sloka_generator_preread,
                    preread_sender=self,
                    context_signal=sloka_generator_context,
                    context_sender=self)
                logger.debug("SlokaGenerator: file: {0}, content: {1}"
                             .format(sloka.source_path, sloka.content))
            except Exception as e:
                logger.warning('SlokaGenerator: Could not process {}'
                               .format(f))
                logger.exception(e)
                continue

            if not is_valid_content(sloka, f):
                continue

            self.articles.append(sloka)

        # TODO sort articles by filename
        # TODO organize articles by chapters
        # TODO link transliterations to original article
        sloka_generator_finalized.send(self)

    def generate_output(self, writer):
        """Generate the sloka file."""
        logger.debug("SlokaGenerator: Generate output")

        for sloka in self.articles:
            override_output = hasattr(sloka, 'override_save_as')
            writer.write_file(name=sloka.save_as,
                              template=self.get_template(sloka.template),
                              context=self.context, sloka=sloka,
                              relative_urls=self.settings['RELATIVE_URLS'],
                              override_output=override_output)
