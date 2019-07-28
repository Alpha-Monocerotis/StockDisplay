from django.shortcuts import render
from django.http import *
# from Stock.plot.plotStock import generate
# Create your views here.
from django.views.generic.base import View
import pandas as pd
from .models import Stock
from .plot.plotStock import zheline
__all__ = ['stock_data', 'TEST_PATH']
stock_data = pd.read_csv('Stock/data/stocks.csv', encoding='gb18030', header=None)

TEST_PATH = "Stock/data/SH/SH000001.csv"

class Refresh_page(View):
    
    @staticmethod
    def get(req: HttpRequest):
        stocks = []
        for i in range(len(stock_data)):
            newStock = Stock()
            newStock.name = stock_data[3].values[i]
            newStock.file = 'Stock' + stock_data[7].values[i][1:] + '%' + newStock.name
            stocks.append(newStock)

        return render(req, 'index2.html', {'stocks': stocks})

    @staticmethod
    def post(req: HttpRequest):
        # print(req.POST)
        stock_name = req.POST['stock-name']
        data = pd.read_csv(stock_name.split('%')[0])
        # data.info()
        stocks = []
        for i in range(len(stock_data)):
            newStock = Stock()
            newStock.name = stock_data[3].values[i]
            newStock.file = 'Stock' + stock_data[7].values[i][1:] + '%' + newStock.name
            stocks.append(newStock)
        linedata1, value1, linedata2, value2 = zheline(high_value=data['High'].values,low_value=data['Low'].values, datetime=data['Date'].values)
        return JsonResponse(data={'status': 'success', 'date': list(data['Date'].values),
                                  'high': list(data['High'].values), 'low': list(data['Low'].values),
                                  'close': list(data['Close'].values), 'open': list(data['Open'].values),
                                  'name': stock_name.split('%')[1], 'upline': value2, 'downline': value1, 'upline_time':linedata2, 'downline_time':linedata1})
    @staticmethod
    def post_scope(req: HttpRequest):
        stock_name = req.POST['stock-name']
        view_scope_start = req.POST['scope-start']
        view_scope_end = req.POST['scope-end']
        
