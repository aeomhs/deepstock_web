from django.shortcuts import render
from ..models import Company, Price, CompanyPrice, PredictedPrice, ScrapyItem
import datetime

# TODO 웹 방문 첫 페이지 구현
# 요소 : 간단한 intro
# 기능 1 다음 페이지 이동 (stock_list.html)
def index(request):
    return render(request, 'demo/welcome.html')


# TODO 종목 리스트 페이지 구현
# 요소 : 설명, 코스피 표, 코스닥 표
# 기능 1 코스피 , 코스닥 각 30 종목씩 리스트업
# 기능 2 종목 선택시 다음 페이지 이동 (stock_analysis.html)
# 기능 3 이전 페이지 이동
def stock_list(request):
    kospi_list = CompanyPrice.objects.get_kospi_stock_list()
    kosdaq_list = CompanyPrice.objects.get_kosdaq_stock_list()

    # Added, 예측 주가 모델 추가
    # 예측 주가 중, 현재 날짜 이후의 값들만 불러온다.
    # 현재는 다음 날의 종가만 예측하기 때문에 문제없지만,
    # 그 이상을 함께 예측할 경우, 한 종목에 대하여 여러 날짜에 대한 예측 값이 넘어갈 수 있다.
    # 이 경우, Templates 쪽에서 헷갈리지 않게, 날짜별로 보여주는 방법이 있다.
    # 혹은, 원하는 날짜에 대해서만 filter할 수도 있다. 이 경우 아래 코드를 수정해야한다.
    predicted_kospi_list = PredictedPrice.objects.filter(company__market_type='kospi', date__gt=datetime.date.today().isoformat())
    predicted_kosdaq_list = PredictedPrice.objects.filter(company__market_type='kosdaq', date__gt=datetime.date.today().isoformat())

    # TEST Fetch Data
    print(predicted_kospi_list)
    print(predicted_kosdaq_list)

    stock_list = {
        'kospi_list' : kospi_list,
        'kosdaq_list' : kosdaq_list,
    }

    return render(request, 'demo/stock_list.html', {'stock_list':stock_list})


# TODO 종목 분석 페이지 구현
# 요소 : 그래프, 설명, 관련 뉴스
# 기능 1 종목의 주가 예측 그래프 제공
# 기능 2 종목 관련 뉴스 제공
# 기능 3 이전 페이지 이동
def stock_analysis(request, stock_code):
    # stock_list 에서 선택된 종목 코드 인자값으로 받아온다. : stock_code
    # 종목이름, 가격리스트, 예측 가격리스트, 관련 뉴스 리스트
    stock_name = Company.objects.get(code=stock_code)
    price_list = Price.objects.filter(company__code=stock_code)[:30] # 최대 30개
    predicted_price_list = PredictedPrice.objects.filter(company__code=stock_code)[:30]
    relevant_news_list = ScrapyItem.objects.filter(stock_code=stock_code)[:10] # 최대 10개의 뉴스만 가져온다.

    # TEST Fetch Data
    print("주식 종목 : ", stock_name)
    for price_date in price_list:
        print(price_date.date, price_date.price)
    for price_date in predicted_price_list:
        print(price_date.date, price_date.price)
    for news in relevant_news_list:
        print(news.date, news.title, news.info, news.url)

    stock_data = {
        'name': stock_name,
        'price_list': price_list,
        'predicted_price_list': predicted_price_list,
        'relevant_news_list': relevant_news_list,
    }

    return render(request, 'demo/stock_analysis.html', {'stock_data': stock_data})
