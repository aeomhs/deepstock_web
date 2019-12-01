from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stock_list/', views.stock_list, name='stock_list'),
    # stock type (코스피 | 코스닥)
    # index (각 표에서 몇 번째인지)
    path('stock_analysis/<int:stock_code>/', views.stock_analysis, name='stock_analysis'),
    path('api/crawl/', views.scrapy_views.crawl, name='crawl'),
]