import json
from django.db import models
from django.utils import timezone

class KospiCompanyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(market_type='KP')

class KosdaqCompanyMananger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(market_type='KD')

class Company(models.Model):
    # CHOICES
    kospi_type = 'KP'
    kosdaq_type = 'KD'
    MARKET_TYPE_CHOICES = (
        (kospi_type, '코스피'),
        (kosdaq_type, '코스닥'),
    )

    name = models.CharField(verbose_name='종목명',max_length=30)
    code = models.CharField(verbose_name='종목 코드',max_length=6)
    market_type = models.CharField(verbose_name='소속',max_length=2,choices=MARKET_TYPE_CHOICES)  

    objects = models.Manager()
    kospi_companies = KospiCompanyManager()
    kosdaq_companies = KosdaqCompanyMananger()

    class Meta:
        verbose_name='종목'
        verbose_name_plural='주식 종목'
        ordering=['name']

    def __str__(self):
        return self.name

class CompanyPriceManager(models.Manager):
    def get_kospi_stock_list(self):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.name, c.code, p.price
                FROM demo_company c, demo_price p
                WHERE c.id = p.company_id AND
                      p.date = (
                          SELECT MAX(p2.date)
                          FROM demo_price p2
                          WHERE p.company_id = p2.company_id
                          GROUP BY p2.company_id
                      ) AND
                      c.market_type = 'KP'
                """)
            result_list = []
            for row in cursor.fetchall():
                p = self.model(id=row[0], name=row[0], code=row[1], price=row[2])
                result_list.append(p)
        return result_list

    def get_kosdaq_stock_list(self):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.name, c.code, p.price
                FROM demo_company c, demo_price p
                WHERE c.id = p.company_id AND
                      p.date = (
                          SELECT MAX(p2.date)
                          FROM demo_price p2
                          WHERE p.company_id = p2.company_id
                          GROUP BY p2.company_id
                      ) AND
                      c.market_type = 'KD'
                """)
            result_list = []
            for row in cursor.fetchall():
                p = self.model(id=row[0], name=row[0], code=row[1], price=row[2])
                result_list.append(p)
        return result_list

class CompanyPrice(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=6)
    price = models.IntegerField()
    
    objects = CompanyPriceManager()

class Price(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name='종목',
    )

    date = models.DateField(
        verbose_name='날짜',
    )

    price = models.IntegerField(
        verbose_name='시가',
    )
    
    objects = models.Manager()
    
    class Meta:
        verbose_name='주가'
        verbose_name_plural='날짜별 주가'
        # 날짜별 각 종목의 시가는 단 하나의 칼럼으로 이루어진다.
        unique_together=(('company', 'date'),)
        ordering=['-date']
        
    def __str__(self):
        return "["+self.company.__str__()+"]"+self.date.strftime('%Y/%m/%d')


# https://medium.com/@ali_oguzhan/how-to-use-scrapy-with-django-application-c16fabd0e62e
class ScrapyItem(models.Model):
    unique_id = models.CharField(max_length=100, null=True)
    data = models.TextField() # this stands for our crawled data
    date = models.DateTimeField(default=timezone.now)
    
    # This is for basic and custom serialisation to return it to client as a JSON.
    @property
    def to_dict(self):
        data = {
            'data': json.loads(self.data),
            'date': self.date
        }
        return data

    def __str__(self):
        return self.unique_id


# class NewsItem(models.Model):
#     stock_code = models.CharField(
#         verbose_name='종목',
#         max_length=6,
#     )
#     title = models.TextField(
#         verbose_name='기사제목',
#     )
#     url = models.TextField(
#         verbose_name='링크',
#     )
#     site = models.CharField(
#         verbose_name='정보제공',
#         max_length=20,
#     )
#     date = models.DateField(
#         verbose_name='날짜',
#     )

#     # This is for basic and custom serialisation to return it to client as a JSON.
#     @property
#     def to_dict(self):
#         data = {
#             'data': json.loads(self.data),
#             'date': self.date
#         }
#         return data

#     def __str__(self):
#         return "["+self.site.__str__()+"]"+self.title.__str__()
