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


def filter_respondents(value):
    result = value.strip('\n').strip('\r').strip(' ').strip(';').replace("\r\n", "")
    result = result.split("See also")[0]
    if len(result) > 2:
        # result = "{word}-[{length}]".format(word=result, length=len(result))
        return result


class Litigation(scrapy.Item):
    release_no = scrapy.Field()
    date = scrapy.Field(
        input_processor=MapCompose(remove_tags)
    )
    respondents = scrapy.Field(
        input_processor=MapCompose(remove_tags, filter_respondents),
        # output_processor=Join()
    )
    title = scrapy.Field()
    subtitle = scrapy.Field()
    contents = scrapy.Field()


class Reference(scrapy.Item):
    litigation = scrapy.Field()
    reference = scrapy.Field()
    reference_text = scrapy.Field()
