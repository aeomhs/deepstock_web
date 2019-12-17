from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stock_list/', views.stock_list, name='stock_list'),
    # stock type (코스피 | 코스닥)
    # index (각 표에서 몇 번째인지)
    re_path(r'^stock_analysis/(?P<stock_code>[0-9]{6})/(?P<predict_price>\d+)/$', views.stock_analysis, name='stock_analysis'),

    # Crawling API
    path('api/crawl/', views.scrapy_views.crawl, name='crawl'),
    path('api/stock_init/', views.scrapy_views.stock_init, name='stock_init'),
]
