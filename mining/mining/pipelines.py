# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from litigations.models import Litigation, Reference, Title
from datetime import datetime
from w3lib.html import remove_tags


def try_parsing_date(text):
    b = text
    text = text.lower().replace(" ", "").replace(".", "").replace(",", "").replace("\n", "").replace("\r", "")

    text = list(text)
    if text is not None and text != "" and text[3] == 's':
        text.pop(3)
    text = str("".join(text))

    formats = ["%b%d%Y", "%B%d%Y"]
    for fmt in formats:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass

        # print("Before: {0}".format(b))
        # print("After: {0}".format(text))
    return None


class MiningPipeline(object):

    def __init__(self):
        self.count = 0

    def process_item(self, item, spider):
        if not spider.name == "detail":
            litigation = Litigation()
            litigation.release_no = item.get("release_no")
            litigation.date = item.get("date")
            litigation.respondents = item.get("respondents")
            litigation.content = item.get("content")
            litigation.save()

            # Titles

            if item.get("h1s") is not None:
                for h1 in item.get("h1s"):
                    if not h1.replace("\r", "").replace("\n", "") == "":
                        title = Title()
                        title.litigation = litigation
                        title.priority = 1
                        title.title_text = h1
                        title.save()

            if item.get("h2s") is not None:
                for h2 in item.get("h2s"):
                    if not h2.replace("\r", "").replace("\n", "") == "":
                        title = Title()
                        title.litigation = litigation
                        title.priority = 2
                        title.title_text = h2
                        title.save()

            if item.get("h3s") is not None:
                for h3 in item.get("h3s"):
                    if not h3.replace("\r", "").replace("\n", "") == "":
                        title = Title()
                        title.litigation = litigation
                        title.priority = 3
                        title.title_text = h3
                        title.save()

            # References

            if item.get("references_names") is not None and item.get("references_urls") is not None:
                for text, url in zip(item.get("references_names"), item.get("references_urls")):
                    reference = Reference()
                    reference.litigation = litigation
                    reference.reference_text = text
                    reference.reference = url
                    reference.save()

            if item.get("references_sidebar_names") is not None and item.get("references_sidebar_urls") is not None:
                for text, url in zip(item.get("references_sidebar_names"), item.get("references_sidebar_urls")):
                    reference = Reference()
                    reference.litigation = litigation
                    reference.reference_text = text
                    reference.reference = url
                    reference.save()


'''
references_names = scrapy.Field()
references_urls = scrapy.Field(input_processor=MapCompose(relative_to_absolute_url))
references_sidebar_names = scrapy.Field()
references_sidebar_urls = scrapy.Field(input_processor=MapCompose(relative_to_absolute_url))
'''




