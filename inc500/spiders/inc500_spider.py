from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider

from inc500.items import Inc500Item

class Inc500Spider(BaseSpider):
    name = 'inc500'
    allowed_domains = ['www.inc.com']
    start_urls = ['http://www.inc.com/inc5000/list/2011/']

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        detail_links = hxs.select('//table[@id="fulltable"]/tr/td/a/@href')
        for link in detail_links:
            item = Inc500Item()
            item_url = link.extract()
            yield Request(item_url, callback=self.parse_item)

        next_url = hxs.select('//div[@class="total_pg"]/span/a[@class="next"]/@href').extract()
        if next_url:
            yield Request(next_url[0], callback=self.parse)


    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)

        item = Inc500Item()
        item['rank'] = int(hxs.select('//div[@class="company_rank"]/text()').extract()[0].strip('#'))
        item['company_name'] = hxs.select('//h1[@class="company_name"]/text()')[0].extract()
        item['blurb'] = hxs.select('//div[@id="company_blurb"]/p/text()')[0].extract().strip()

        table_rows = hxs.select('//tr[@class="employees"]')

        for row in table_rows:
            extract = row.extract()
            if '3-year growth:' in extract:
                item['three_year_pct_growth'] = row.select('td/span[@class="right"]/text()')[0].extract().strip('%')
            elif '2010 Revenue:' in extract:
                item['revenue_2010'] = self._parse_num(row.select('td/span[@class="right"]/text()')[0].extract())
            elif '2007 Revenue:' in extract:
                item['revenue_2007'] = self._parse_num(row.select('td/span[@class="right"]/text()')[0].extract())
            elif 'Employees:' in extract:
                item['num_employees'] = int(row.select('td/span[@class="right"]/text()')[0].extract())
            elif 'Employee growth:' in extract:
                item['employee_growth'] = int(row.select('td/span[@class="right"]/text()')[0].extract())
            elif 'Founded:' in extract:
                item['founded'] = int(row.select('td/span[@class="right"]/text()')[0].extract())
            elif 'Industry:' in extract:
                item['industry'] = row.select('td/span[@class="right indyblock"]/text()')[0].extract()[1:]
            elif 'Industry rank:' in extract:
                item['industry_rank'] = int(row.select('td/span[@class="right"]/text()')[0].extract().strip('#'))

        item['link'] = hxs.select('//div[@class="website-state"]/small[@class="company_site"]/a/@href').extract()[0]

        location = hxs.select('//div[@class="website-state"]/small[@class="local"]/text()')[0].extract()
        location = map(lambda s: s.strip(), location.split(','))
        state = location[-1]
        city = ', '.join(location[0:-1])

        item['city'] = city
        item['state'] = state

        yield item

    def _parse_num(self, num_str):
        if 'million' in num_str:
            num = float(num_str.strip('million $'))
            return num * 1000000
        elif 'billion' in num_str:
            num = float(num_str.strip('billion $'))
            return num * 1000000000
        else:
            num = float(''.join(num_str.strip('$').split(',')))
            return num

