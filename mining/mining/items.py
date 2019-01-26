# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags


class MiningItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def relative_to_absolute_url(value):
    return "https://www.sec.gov/{0}".format(value)


def filter_respondents(value):
    result = value.strip('\n').strip('\r').strip(' ').strip(';').replace("\r\n", "")
    result = result.split("See also")[0]
    if len(result) > 2:
        # result = "{word}-[{length}]".format(word=result, length=len(result))
        return result


def fix_unicode(value):
    return value.encode('utf-8')


class Litigation(scrapy.Item):
    release_no = scrapy.Field(
        # input_processor=
    )
    date = scrapy.Field(
        input_processor=MapCompose(remove_tags)
    )
    respondents = scrapy.Field(
        input_processor=MapCompose(remove_tags, filter_respondents)
    )
    title = scrapy.Field(
        # input_processor=
    )
    subtitle = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join('\n')
    )
    content = scrapy.Field(
        input_processor=Join('\n')
    )
    references_names = scrapy.Field()
    references_urls = scrapy.Field()
    references_sidebar_names = scrapy.Field()
    references_sidebar_urls = scrapy.Field(input_processor=MapCompose(relative_to_absolute_url))

    # def __str__(self) -> str:
    #     return "{content}-[{length}]".format(self.content, len(self.content))


class Reference(scrapy.Item):
    litigation = scrapy.Field()
    reference = scrapy.Field()
    reference_text = scrapy.Field()
