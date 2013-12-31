# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import logging

from pelican.generators import Generator
from pelican.contents import Content, is_valid_content

from prajna.signals import *

logger = logging.getLogger(__name__)

class Sloka(Content):
    mandatory_properties = ('text',)
    default_template = 'page'


class SlokaGenerator(Generator):
    """Generate pages"""

    def __init__(self, *args, **kwargs):
        super(SlokaGenerator, self).__init__(*args, **kwargs)
        #signals.page_generator_init.send(self)

    def generate_context(self):
        """Add the articles into the shared context"""
        #signals.page_generator_finalized.send(self)
        #import pudb
        #pudb.set_trace()
        print("generate context")

        all_articles = []
        for f in self.get_files(
                self.settings['SLOKA_DIR'],
                exclude=self.settings['SLOKA_EXCLUDES']):
            try:
                sloka = self.readers.read_file(
                    base_path=self.path, path=f, content_class=Sloka,
                    context=self.context,
                    preread_signal=sloka_generator_preread,
                    preread_sender=self,
                    context_signal=sloka_generator_context,
                    context_sender=self)
                print("file: {0}, content: {1}", sloka.source_path, sloka.content)
            except Exception as e:
                logger.warning('Could not process {}\n{}'.format(f, e))
                continue

            if not is_valid_content(sloka, f):
                continue

            #self.add_source_path(article)

            #if article.status == "published":
                #all_articles.append(article)
            #elif article.status == "draft":
                #self.drafts.append(article)
            #else:
                #logger.warning("Unknown status %s for file %s, skipping it." %
                               #(repr(article.status),
                                #repr(f)))

        #self.articles, self.translations = process_translations(all_articles)

        #for article in self.articles:
            ## only main articles are listed in categories and tags
            ## not translations
            #self.categories[article.category].append(article)
            #if hasattr(article, 'tags'):
                #for tag in article.tags:
                    #self.tags[tag].append(article)
            ## ignore blank authors as well as undefined
            #if hasattr(article, 'author') and article.author.name != '':
                #self.authors[article.author].append(article)


        ## sort the articles by date
        #self.articles.sort(key=attrgetter('date'), reverse=True)
        #self.dates = list(self.articles)
        #self.dates.sort(key=attrgetter('date'),
                #reverse=self.context['NEWEST_FIRST_ARCHIVES'])

        ## create tag cloud
        #tag_cloud = defaultdict(int)
        #for article in self.articles:
            #for tag in getattr(article, 'tags', []):
                #tag_cloud[tag] += 1

        #tag_cloud = sorted(tag_cloud.items(), key=itemgetter(1), reverse=True)
        #tag_cloud = tag_cloud[:self.settings.get('TAG_CLOUD_MAX_ITEMS')]

        #tags = list(map(itemgetter(1), tag_cloud))
        #if tags:
            #max_count = max(tags)
        #steps = self.settings.get('TAG_CLOUD_STEPS')

        ## calculate word sizes
        #self.tag_cloud = [
            #(
                #tag,
                #int(math.floor(steps - (steps - 1) * math.log(count)
                    #/ (math.log(max_count)or 1)))
            #)
            #for tag, count in tag_cloud
        #]
        ## put words in chaos
        #random.shuffle(self.tag_cloud)

        ## and generate the output :)

        ## order the categories per name
        #self.categories = list(self.categories.items())
        #self.categories.sort(
                #reverse=self.settings['REVERSE_CATEGORY_ORDER'])

        #self.authors = list(self.authors.items())
        #self.authors.sort()

        #self._update_context(('articles', 'dates', 'tags', 'categories',
                              #'tag_cloud', 'authors', 'related_posts'))

        sloka_generator_finalized.send(self)
        pass

    def generate_output(self, writer):
        #writer.write_file(page.save_as, self.get_template(page.template),
                          #self.context, page=page,
                          #relative_urls=self.settings['RELATIVE_URLS'],
                          #override_output=hasattr(page, 'override_save_as'))
        #import pudb
        #pudb.set_trace()
        print("generate output")
        pass



