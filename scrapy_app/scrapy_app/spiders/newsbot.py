# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


'''
 TODO stock_code에 따라 다른 뉴스 크롤링
 ISSUE 파싱을 특정 사이트 기준으로 진행하기때문에, 다른 사이트 url 혹은 사이트 태그 달라지면 에러 발생
'''
class NewsbotSpider(CrawlSpider):
    name = 'newsbot'
    
    base_url = 'https://finance.naver.com'

    def __init__(self, *args, **kwargs):
        # We are going to pass these args from our django view.
        # To make everything dynamic, we need to override them inside __init__ method
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]

        NewsbotSpider.rules = [
           Rule(LinkExtractor(unique=True), callback='parse_item'),
        ]
        super(NewsbotSpider, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        # You can tweak each crawled page here
        # Don't forget to return an object.
        titles = response.xpath('//*[@class="title"]/a/text()').extract()
        urls = response.xpath('//*[@class="title"]/a/@href').extract()
        infos = response.xpath('//*[@class="info"]/text()').extract()
        dates = response.xpath('//*[@class="date"]/text()').extract()
        
        for item in zip(titles, urls, infos, dates):
            scraped_info = {
                'title': item[0].strip(),
                'url': self.base_url + item[1].strip(),
                'info': item[2].strip(),
                'date': item[3].strip(),
            }
            yield scraped_info
        
        return {'titles': titles, 'urls': urls, 'infos': infos, 'dates': dates}
