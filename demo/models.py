from django.db import models

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
    def get_queryset(self, _company):
        return super().get_queryset().filter(company=_company)

class Price(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name='종목명',
    )

    date = models.DateField(
        verbose_name='날짜',
    )

    price = models.IntegerField(
        verbose_name='시가',
    )
    
    objects = models.Manager()
    company_price = CompanyPriceManager()

    class Meta:
        verbose_name='주가'
        verbose_name_plural='날짜별 주가'
        # 날짜별 각 종목의 시가는 단 하나의 칼럼으로 이루어진다.
        unique_together=(('company', 'date'),)
        ordering=['company']
        
    def __str__(self):
        return "["+self.company.__str__()+"]"+self.date.strftime('%Y/%m/%d')