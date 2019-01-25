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
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')


class MiningPipeline(object):

    def process_item(self, item, spider):
        # print(item)
        release_no, date, respondents = item["row"]

        litigation = Litigation()
        litigation.release_no = release_no
        litigation.date = try_parsing_date(date).date()
        litigation.respondents = respondents
        litigation.save()

        # print(litigation)
        # print("Django Length:")
        # print(len(item['release_no']))
        # print(len(item['date']))
        # print(len(item['respondents']))
        # (rels, dates, resps) = item.values()

        # for i in range(0, len(rels)):
        # litigation = Litigation()
        # litigation.release_no = rels[i]
        # litigation.date = datetime.datetime.strptime(dates[i], "%b. %d, %Y").date()
        # litigation.respondents = resps[i]

        # try:
        #
        #     litigation = Litigation.objects.get(release_no=item["release_no"])
        #     return item
        # except Litigation.DoesNotExist:
        #     pass

        # Comment Ctrl + /

        # litigation = Litigation()
        # litigation.release_no = item["release_no"][i]
        # litigation.date = datetime.datetime.strptime(item["date"][i], "%b. %d, %Y").date()
        # litigation.respondents = item["respondents"][i]
        # print("{} - {}".format(i, litigation))
        # litigation = Litigation()
        # litigation.release_no = item["release_no"][i]
        # litigation.date = datetime.datetime.strptime(item["date"][i], "%b. %d, %Y").date()
        # litigation.respondents = item["respondents"][i]
        # print("{} - {}".format(i, litigation))
