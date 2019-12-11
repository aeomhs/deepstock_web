# -*- coding: utf-8 -*-
import scrapy, json
from scrapy.linkextractors import LinkExtractor


class StockbotSpider(scrapy.Spider):
    name = 'stockbot'
    allowed_domains = ['playstyle.s3.ap-northeast-2.amazonaws.com']
    start_urls = ['https://playstyle.s3.ap-northeast-2.amazonaws.com/']

    def __init__(self, *args, **kwargs):
        # We are going to pass these args from our django view.
        # To make everything dynamic, we need to override them inside __init__ method
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]

        self.logger.info('stock bot init')

        super(StockbotSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        stock_item = json.loads(response.text)
        self.logger.info('stock crawler parsed : %s', stock_item['stock_name'])

        scraped_info = {
            'stock_name': stock_item['stock_name'],
            'market_type': stock_item['market_type'],
            'stock_code': stock_item['stock_code'],
            'price': stock_item['price'],
            'price_date': stock_item['price_date'],
            'predict': stock_item['predict'],
            'predict_date': stock_item['predict_date'],
        }

        return scraped_info
