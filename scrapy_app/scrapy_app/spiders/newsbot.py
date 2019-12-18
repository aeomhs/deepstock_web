# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

import json
from urllib.request import urlopen


# stock_code에 따라 다른 뉴스 크롤링 || stock_code == all 일경우 모든 종목 뉴스 크롤링
class NewsbotSpider(CrawlSpider):
    name = 'newsbot'
    
    base_url = 'https://finance.naver.com'

    def __init__(self, *args, **kwargs):
        # We are going to pass these args from our django view.
        # To make everything dynamic, we need to override them inside __init__ method
        self.stock_code = kwargs.get('stock_code')
        crawl_base_url = 'https://finance.naver.com/item/news_news.nhn'
        self.start_urls = []

        # 모든 종목별 뉴스 스크랩 진행
        if self.stock_code == 'all':
            # s3 Stock Code list 받아오기
            info_url = 'https://playstyle.s3.ap-northeast-2.amazonaws.com/items_info.json'
            stock_info_json = json.loads(urlopen(info_url).read())

            # 모든 종목에 대한 관련 뉴스 URL Parsing
            for stock in stock_info_json.values():
                self.start_urls.append(
                    crawl_base_url + '?code=' + stock['code'] + '&page=1&sm=title_entity_id.basic&clusterId='
                )
        # stock_code 관련 뉴스 스크랩
        else:
            self.start_urls = [
                crawl_base_url + '?code=' + self.stock_code + '&page=1&sm=title_entity_id.basic&clusterId='
            ]

        self.allowed_domains = [
            'finance.naver.com'
        ]

        NewsbotSpider.rules = [
           Rule(LinkExtractor(unique=True), callback='parse_item'),
        ]
        super(NewsbotSpider, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        # You can tweak each crawled page here
        # Don't forget to return an object.
        stock_code = response.url.split('?')[1].split('=')[1].split('&')[0]
        titles = response.xpath('//*[@class="title"]/a/text()').extract()
        urls = response.xpath('//*[@class="title"]/a/@href').extract()
        infos = response.xpath('//*[@class="info"]/text()').extract()
        dates = response.xpath('//*[@class="date"]/text()').extract()
        
        for item in zip(titles, urls, infos, dates):
            scraped_info = {
                'stock_code': stock_code,
                'title': item[0].strip(),
                'url': self.base_url + item[1].strip(),
                'info': item[2].strip(),
                'date': item[3].strip(),
            }
            yield scraped_info
        
        return {'stock_code': self.stock_code, 'titles': titles, 'urls': urls, 'infos': infos, 'dates': dates}
