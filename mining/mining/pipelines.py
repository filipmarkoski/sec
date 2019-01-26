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

    def process_item(self, item, spider):
        # print(item)
        release_no, date, respondents = item["row"]

        litigation = Litigation()
        litigation.release_no = release_no
        litigation.date = try_parsing_date(date)
        litigation.respondents = respondents
        litigation.save()
