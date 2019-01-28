import os
import scrapy
from scrapy.loader import ItemLoader
from mining.items import Litigation
from mining.pipelines import try_parsing_date


class LitigationsDetailSpider(scrapy.Spider):
    name = "detail"

    def start_requests(self):
        start_urls = [
            # 'https://www.sec.gov/litigation/litreleases.shtml'
        ]

        request_2019 = scrapy.Request(url='https://www.sec.gov/litigation/litreleases.shtml',
                                      callback=self.parse_master)
        request_2019.meta["year"] = 2019
        yield request_2019

        # for year in range(1995, 2019):
        for year in range(1995, 2019):
            url = 'https://www.sec.gov/litigation/litreleases/litrelarchive/litarchive{year}.shtml'.format(year=year)
            request_master = scrapy.Request(url=url, callback=self.parse_master)
            request_master.meta["year"] = year
            yield request_master

    def parse_master(self, response):
        # response = response.replace(encoding='iso-8859-1')
        # response = response.replace(encoding='utf-8')

        year = response.meta.get("year")

        item_loader = ItemLoader(item=Litigation(), response=response)

        if year > 2006:
            item_loader.add_xpath('release_no',
                                  '//tr[count(@id) = 0]/td[1]/a[contains(text(), "LR")] | ' +
                                  '//tr[count(@id) = 0]/td[1][contains(text(), "LR")]')
            item_loader.add_xpath('date', '//tr[count(@id) = 0]/td[2]')
            item_loader.add_xpath('respondents', '//tr[count(@id) = 0]/td[3]')
        else:
            item_loader.add_xpath('release_no',
                                  '(//table)[5]/tr[count(@id) = 0]/td[1]/a[contains(text(), "LR-")]')
            item_loader.add_xpath('date', '(//table)[5]/tr[count(@id) = 0]/td[2]')
            item_loader.add_xpath('respondents', '(//table)[5]/tr[count(@id) = 0]/td[3]')

        rels, dates, resps = item_loader.load_item().values()

        if year > 2006:
            pass
        else:
            # rels.pop(0)
            dates.pop(0)
            resps.pop(0)

        print(rels[0])
        print(rels[-1])

        print(dates[0])
        print(dates[-1])

        print(resps[0])
        print(resps[-1])

        print(len(rels))
        print(len(dates))
        print(len(resps))

        for i in range(int(len(rels))):
            code = rels[i].lower()

            item = Litigation()
            item['date'] = try_parsing_date(dates[i])
            item['release_no'] = rels[i]
            item['respondents'] = resps[i]

            if item.get("date") is None:  # for Omitted

                path = "//tr[count(@id) = 0]/td[1]/a[text()='{rel_no}']".format(rel_no=rels[i])
                result = response.xpath(path)
                if len(result) != 0:
                    request = scrapy.Request(
                        url='https://www.sec.gov/litigation/litreleases/lr{code}.txt'.format(code=code[3:]),
                        callback=self.parse_detail)
                    request.meta["item"] = item
                    yield request
                else:
                    item["content"] = None
                    item["references_names"] = None
                    item["references_urls"] = None
                    item["references_sidebar_names"] = None
                    item["references_sidebar_urls"] = None
                    yield item

            else:  # for the normal ones
                if year >= 2006:
                    request = scrapy.Request(
                        url='https://www.sec.gov/litigation/litreleases/{year}/lr{code}.htm'
                            .format(year=year,
                                    code=code[3:]),
                        callback=self.parse_detail)
                else:
                    if item.get("date") >= try_parsing_date("May 20, 1999"):
                        request = scrapy.Request(
                            url='https://www.sec.gov/litigation/litreleases/lr{code}.htm'.format(code=code[3:]),
                            callback=self.parse_detail)
                    else:
                        request = scrapy.Request(
                            url='https://www.sec.gov/litigation/litreleases/lr{code}.txt'.format(code=code[3:]),
                            callback=self.parse_detail)

                request.meta["item"] = item
                yield request

    def parse_detail(self, response):
        item = response.meta["item"]  # item is of type Litigation

        item_loader = ItemLoader(item=Litigation(), response=response)

        if item.get("date") is not None and item.get("date") >= try_parsing_date("May 20, 1999"):
            if item.get("date").year >= 2016:
                item_loader.add_xpath('h1s', '//h1 | //h1/p | //h1/a')
                item_loader.add_xpath('h2s', '//h2 | //h2/p | //h2/a')
                item_loader.add_xpath('h3s', '//h3 | //h3/p | //h3/a')
                item_loader.add_xpath('references_names', '//div[@class="grid_7 alpha"]/p/a/text()')
                item_loader.add_xpath('references_urls', '//div[@class="grid_7 alpha"]/p/a/@href')
                item_loader.add_xpath('references_sidebar_names', '//div[@class="grid_3 omega"]/ul/li/a/text()')
                item_loader.add_xpath('references_sidebar_urls', '//div[@class="grid_3 omega"]/ul/li/a/@href')
                item_loader.add_xpath('content', '//div[@class="grid_7 alpha"]/p')
            else:
                item_loader.add_xpath('h1s', '//h1 | //h1/p | //h1/a')
                item_loader.add_xpath('h2s', '//h2 | //h2/p | //h2/a')
                item_loader.add_xpath('h3s', '//h3 | //h3/p | //h3/a')
                item_loader.add_xpath('references_names',
                                      '//p/a/text() | ((//table)[3]/tr/td[3]/font/table)[position() < last()]//tr/td/a/text()')
                item_loader.add_xpath('references_urls',
                                      '//p/a/@href | ((//table)[3]/tr/td[3]/font/table)[position() < last()]//tr/td/a/@href')
                item_loader.add_xpath('content', '//p | //li')

        else:
            item_loader.add_xpath('content', '//body')

        item_details = item_loader.load_item()
        item.update(item_details)
        return item
