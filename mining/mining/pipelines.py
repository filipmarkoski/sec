# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from litigations.models import Litigation, Reference
import datetime
import time


class MiningPipeline(object):

    def process_item(self, item, spider):
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
        item.save()
        return item
