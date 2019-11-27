from django.db import models

class Company(models.Model):
    name = models.CharField(verbose_name='종목명',max_length=30)
    code = models.CharField(verbose_name='종목 코드',max_length=6)
    price = models.IntegerField(verbose_name='전일 종가')
    biz_type = models.CharField(verbose_name='업종',max_length=20)
    market_type = models.CharField(verbose_name='소속',max_length=2)

    class Meta:
        verbose_name='종목'
        verbose_name_plural='주식 종목'
        ordering=['-price']

class PredictedPrice(models.Model):
    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        verbose_name='종목명',
    )
    now = models.IntegerField(verbose_name='전일 종가')
    tomorrow = models.IntegerField(verbose_name='명일 예측 종가')
    after_a_month = models.IntegerField(verbose_name='명월 예측 종가')
    
    class Meta:
        verbose_name='종목 주가 예측'
        verbose_name_plural='예측 주가'
        ordering=['-now']
