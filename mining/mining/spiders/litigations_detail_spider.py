import os
import scrapy
from scrapy.loader import ItemLoader
from mining.items import Litigation
from mining.pipelines import try_parsing_date


class LitigationsDetailSpider(scrapy.Spider):
    name = "detail"

    def start_requests(self):

        start_urls = [
            'https://www.sec.gov/litigation/litreleases.shtml'
        ]
        for i in range(2018, 2019):
            start_urls.append('https://www.sec.gov/litigation/litreleases/litrelarchive/litarchive{0}.shtml'.format(i))

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_master)

    def parse_master(self, response):

        response = response.replace(encoding='iso-8859-1')
        response = response.replace(encoding='utf-8')

        codes = response.xpath('//tr[count(@id) = 0]/td[1]/a[contains(.//text(), "LR")]/text()').extract()
        date_as_string = response.xpath('//tr[count(@id) = 0]/td[2]/text()')[0].extract()
        actual_date = try_parsing_date(date_as_string)
        year = actual_date.year

        item_loader = ItemLoader(item=Litigation(), response=response)
        item_loader.add_xpath('release_no',
                              '//tr[count(@id) = 0]/td[1]/a/text() | //tr[count(@id) = 0]/td[1]/text()')
        item_loader.add_xpath('date', '//tr[count(@id) = 0]/td[2]')
        item_loader.add_xpath('respondents', '//tr[count(@id) = 0]/td[3]')

        rels, dates, resps = item_loader.load_item().values()

        # WATCH OUT
        # INTEGER DIVISION

        for i in range(int(len(rels))):
            code = rels[i].lower()
            if year >= 2006:
                item = Litigation()
                item['date'] = try_parsing_date(dates[i])
                item['release_no'] = rels[i]
                item['respondents'] = resps[i]

                if item["date"] is None:
                    item["title"] = None
                    item["subtitle"] = None
                    item["content"] = None
                    item["references_names"] = None
                    item["references_urls"] = None
                    item["references_sidebar_names"] = None
                    item["references_sidebar_urls"] = None
                    yield item
                else:
                    request = scrapy.Request(
                        url='https://www.sec.gov/litigation/litreleases/{year}/lr{code}.htm'
                            .format(year=year,
                                    code=code[3:]),
                        callback=self.parse_detail)

                    request.meta["item"] = item
                    yield request

            else:
                yield scrapy.Request(
                    url='https://www.sec.gov/litigation/litreleases/lr{code}.htm'.format(code=code[3:]),
                    callback=self.parse_detail)

    def parse_detail(self, response):
        item = response.meta["item"]  # item is of type Litigation

        item_loader = ItemLoader(item=Litigation(), response=response)

        item_loader.add_xpath('titles', '//h1/text()')
        item_loader.add_xpath('references_names', '//div[@class="grid_7 alpha"]/p/a/text()')
        item_loader.add_xpath('references_urls', '//div[@class="grid_7 alpha"]/p/a/@href')
        item_loader.add_xpath('references_sidebar_names', '//div[@class="grid_3 omega"]/ul/li/a/text()')
        item_loader.add_xpath('references_sidebar_urls', '//div[@class="grid_3 omega"]/ul/li/a/@href')
        item_loader.add_xpath('content',
                              '//div[@class="grid_7 alpha"]/p/text() | //div[@class="grid_7 alpha"]/p/a/text()')

        item_details = item_loader.load_item()
        item.update(item_details)
        return item
