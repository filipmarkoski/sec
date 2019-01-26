import scrapy
from mining.items import Litigation, Reference
from scrapy.loader import ItemLoader


class LitigationsMasterSpider(scrapy.Spider):
    name = "master"

    def start_requests(self):
        urls = [
            # "https://www.sec.gov/litigation/litreleases.shtml",
            "https://www.sec.gov/litigation/litreleases/litrelarchive/litarchive2018.shtml",

        ]

        '''for year in range(1995, 2018 + 1):
            urls.append("https://www.sec.gov/litigation/litreleases/litrelarchive/litarchive{year}.shtml".format(year=year))
'''
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item_loader = ItemLoader(item=Litigation(), response=response)
        item_loader.add_xpath('release_no', '//tr[count(@id) = 0]/td[1]/a/text() | //tr[count(@id) = 0]/td[1]/text()')
        item_loader.add_xpath('date', '//tr[count(@id) = 0]/td[2]')
        item_loader.add_xpath('respondents', '//tr[count(@id) = 0]/td[3]')

        rels, dates, resps = item_loader.load_item().values()

        # print(len(rels))
        # print(len(dates))
        # print(len(resps))

        for row in zip(rels, dates, resps):
            yield {"row": row}

        return
