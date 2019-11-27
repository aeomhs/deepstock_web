from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('welcome', views.welcome, name='welcome'),
    path('stock_list', views.stock_list, name='stock_list'),
    # stock type (코스피 | 코스닥)
    # index (각 표에서 몇 번째인지)
    path('stock_analysis', views.stock_analysis, name='stock_analysis'),
]