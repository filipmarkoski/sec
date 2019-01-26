# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from litigations.models import Litigation, Reference
from datetime import datetime


def try_parsing_date(text):
    for fmt in ("%b. %d, %Y", "%b %d, %Y"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    return None
    # raise ValueError('no valid date format found')


class MiningPipeline(object):

    def __init__(self):
        self.count = 0

    def process_item(self, item, spider):

        if spider.name == "master":
            release_no, date, respondents = item["row"]

            litigation = Litigation()
            litigation.release_no = release_no
            litigation.date = try_parsing_date(date)
            litigation.respondents = respondents
            print(litigation)
            # litigation.save()

        elif spider.name == "detail":
            print(type(item))
            print(item)

            # print("ITEM NUMBER {0}:\n\t Title: {1}\n\t Subtitle: {2}\n\t Content: {3} \n\tReferences: "
            #       .format(self.count, item['title'], item['subtitle'], item['content']))
            # self.count += 1
            # if len(item['references_names']) != 0:
            #     print("\tFROM CONTENT:")
            #     for i in range(0, len(item['references_names'])):
            #         print("\tname: {0} url: {1}".format(item['references_names'][i], item['references_urls'][i]))
            # if len(item['references_sidebar_names']) != 0:
            #     print("\tFROM SIDEBAR:")
            #     for i in range(0, len(item['references_sidebar_names'])):
            #         print("\tname: {0} url: {1}".format(item['references_sidebar_names'][i],
            #                                             item['references_sidebar_urls'][i]))


