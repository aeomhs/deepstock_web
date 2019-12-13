from django.shortcuts import render
from ..models import Company, Price, CompanyPrice


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


    return render(request, 'demo/stock_analysis.html', {'stock_code':stock_code})