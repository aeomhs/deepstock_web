# -*- coding: utf-8 -*-
import scrapy, json
from urllib.request import urlopen

stock_list = []
info_url = 'https://playstyle.s3.ap-northeast-2.amazonaws.com/items_info.json'
stock_info_json = json.loads(urlopen(info_url).read())
for stock in stock_info_json.values():
    stock_list.append(stock['code'])

# stock_list = [
#     '005930'
# ]

# TODO AWS S3로부터 주식 종목 데이터 및 예측 주가 값 가져오기 기능 통합
# 1. `/api/crawl` POST 요청 발생 {taskID, uniqueID, crawlingStatus, task_type}
# 2. `stock_list.json` file 읽기, `https://playstyle.s3.ap-northeast-2.amazonaws.com/{$STOCK_CODE}.json` url parsing
# 3. url에 대하여 모두 크롤링 시작
# 4. 크롤링 데이터 웹 서버 DB에 저장    # DONE
class StockbotSpider(scrapy.Spider):
    name = 'stockbot'
    base_url = 'https://playstyle.s3.ap-northeast-2.amazonaws.com'
    allowed_domains = ['playstyle.s3.ap-northeast-2.amazonaws.com']
    start_urls = []

    def __init__(self, *args, **kwargs):
        self.logger.info('stock bot init')

        for stock in stock_list:
            self.start_urls.append(self.base_url+'/'+stock+'.json')

        super(StockbotSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        self.logger.info('start parsing at : %s', response.url)
        stock_item = json.loads(response.text)

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
