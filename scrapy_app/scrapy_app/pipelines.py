# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# https://medium.com/@ali_oguzhan/how-to-use-scrapy-with-django-application-c16fabd0e62e
from demo.models import ScrapyItem
from demo.models import Company, Price, PredictedPrice
import logging
from django.db import IntegrityError


# ISSUE 현재 각 뉴스 하나를 object 단위로 저장하기 때문에, db 상당 수 저장된다. 데이터 관리가 어렵다.
# 방법 1. 크롤링할때마다 관련 db를 초기화한다.
# 방법 2. save하기 전, 뉴스 제목으로 검색하여 있으면 저장을 생략한다.
# 방법 3. 날짜별로 크롤링을 진행하여 저장한다.
class ScrapyAppPipeline(object):
    def __init__(self, unique_id, *args, **kwargs):
        self.unique_id = unique_id
        self.items = []

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            unique_id=crawler.settings.get('unique_id'), # this will be passed from django view
        )

    def close_spider(self, spider):
        logger = logging.getLogger(__name__)
        logger.info(spider.name)
        if spider.name == 'newsbot':
            # And here we are saving our crawled data with django models.
            for i in self.items:
                item = ScrapyItem()
                item.unique_id = self.unique_id
                item.stock_code = i['stock_code']
                item.title = i['title']
                item.url = i['url']
                item.info = i['info']
                item.date = i['date']
                item.save()
        elif spider.name == 'stockbot':
            for i in self.items:
                # 종목 정보 저장
                try:
                    company = Company.objects.get(name=i['stock_name'])
                except Company.DoesNotExist:
                    company = Company()
                    company.name = i['stock_name']
                    company.market_type = i['market_type']
                    company.code = i['stock_code']
                    company.save()
                # 종목별 실제 가격 저장
                previous_prices = i['previous_prices']
                for price_date in previous_prices:
                    # logger.info("Saving... %s", price_date)
                    try:
                        price = Price()
                        price.company = company
                        price.price = price_date['price']
                        price.date = price_date['date']
                        price.save()
                    except IntegrityError:
                        price = Price.objects.get(company=company, date=price_date['date'])
                        price.price = price_date['price']
                        price.save()
                        logger.info("Already Exist Data, Price updated")
                # 종목별 예측 가격 저장
                # Modified, 예측 주가 Model 생성
                try:
                    predict = PredictedPrice()
                    predict.company = company
                    predict.price = i['predict_price']['price']
                    predict.date = i['predict_price']['date']
                    predict.save()
                except IntegrityError:
                    predict = PredictedPrice.get(company=company, date=i['predict_price']['date'])
                    predict.date = i['predict_price']['date']
                    predict.save()
                    logger.info("Already Exist Data, Predicted Price updated")

    def process_item(self, item, spider):
        self.items.append(item)

        return item
