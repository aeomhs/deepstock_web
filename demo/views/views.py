from django.shortcuts import render
from ..models import Company, Price, CompanyPrice, PredictedPrice
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
    predicted_kospi_list = list(PredictedPrice.objects.filter(company__market_type='kospi', date__gte=datetime.date.today().isoformat()))
    predicted_kosdaq_list = list(PredictedPrice.objects.filter(company__market_type='kosdaq', date__gte=datetime.date.today().isoformat()))

    # TEST Fetch Data
    # print(predicted_kospi_list)
    # print(predicted_kosdaq_list)

    kospi_data = []
    for i in range(len(predicted_kospi_list)):
        predict_price = custom_filter(predicted_kospi_list, lambda x: x.company.name == kospi_list[i].name)
        kospi_data.append((kospi_list[i], predict_price,
                           round((predict_price - int(kospi_list[i].price))
                                 / int(kospi_list[i].price) * 100.0, 2)))

    kosdaq_data = []
    for i in range(len(predicted_kosdaq_list)):
        predict_price = custom_filter(predicted_kosdaq_list, lambda x: x.company.name == kosdaq_list[i].name)
        kosdaq_data.append((kosdaq_list[i], predict_price,
                            round((predict_price - int(kosdaq_list[i].price))
                                  / int(kosdaq_list[i].price) * 100.0, 2)))

    stock_list = {
        'kospi_list': kospi_data,
        'kosdaq_list': kosdaq_data
    }

    return render(request, 'demo/stock_list.html', {
        'stock_list': stock_list})


def custom_filter(stocks, find_filter):
    for x in stocks:
        if find_filter(x):
            return int(x.price)
    return 0

# TODO 종목 분석 페이지 구현
# 요소 : 그래프, 설명, 관련 뉴스
# 기능 1 종목의 주가 예측 그래프 제공
# 기능 2 종목 관련 뉴스 제공
# 기능 3 이전 페이지 이동
def stock_analysis(request, stock_code, predict_price):
    data_set = sorted(list(Price.objects.filter(company__code=stock_code)), key=lambda x: x.date)
    date_list = []
    price_list = []
    for i in range(len(data_set)):
        date_list.append(data_set[i].date.isoformat())
        price_list.append(data_set[i].price)

    return render(request, 'demo/stock_analysis.html',
                  {'stock_code': stock_code,
                   'stock_name': data_set[0].company.name,
                   'predict_price': predict_price,
                   'date_list': date_list,
                   'price_list': price_list})
