from django.shortcuts import render
from django.http import *
# from Stock.plot.plotStock import generate
# Create your views here.
from django.views.generic.base import View
import pandas as pd
from .models import Stock
from .plot.plotStock import zheline
__all__ = ['stock_name_list', 'TEST_PATH']
stock_name_list = pd.read_csv('Stock/data/stocks.csv', encoding='gb18030', header=None)
# Get stock name and filepath list from csv file.
TEST_PATH = "Stock/data/SH/SH000001.csv"
# TEST_PATH is for testing.
class Refresh_page(View):
    @staticmethod
    def get(req: HttpRequest):
        stocks = []
        for i in range(len(stock_name_list)):
            newStock = Stock()
            newStock.name = stock_name_list[3].values[i]
            newStock.file = 'Stock' + stock_name_list[7].values[i][1:] + '%' + newStock.name
            stocks.append(newStock)

        return render(req, 'index2.html', {'stocks': stocks})

    @staticmethod
    def post(req: HttpRequest):
        stock_name = req.POST['stock-name']
        data = pd.read_csv(stock_name.split('%')[0])
        stocks = []
        linedata1, value1, linedata2, value2 = zheline(high_value=data['High'].values,low_value=data['Low'].values, datetime=data['Date'].values)
        return JsonResponse(data={'status': 'success', 'date': list(data['Date'].values),'high': list(data['High'].values), 'low': list(data['Low'].values),'close': list(data['Close'].values), 'open': list(data['Open'].values),'name': stock_name.split('%')[1], 'upline': value2, 'downline': value1, 'upline_time':linedata2, 'downline_time':linedata1})
        
    @staticmethod
    def post_scope(req: HttpRequest):
        """
        Updated version of post method, the client can appoint the scope they want to view.
            Args:
                req (HttpRequest): Received request from frontend client
            Returns:
                JsonResponse: JSON response with data.
            Raises:
                None
        """
            Tested: False
        stock_name = req.POST['stock-name']
        view_scope_start = req.POST['scope-start']
        view_scope_end = req.POST['scope-end']
        stock_data = pd.read_csv(stock_name.split('%')[0])
        stock_data = stock_data[stock_data.date > view_scope_start]
        data = stock_data[stock_data.date < view_scope_end]
        print(stock_name, data)
        stocks = []
        linedata1, value1, linedata2, value2 = zheline(high_value=data['High'].values,low_value=data['Low'].values, datetime=data['Date'].values)
        return JsonResponse(data={'status': 'success', 'date': list(data['Date'].values),'high': list(data['High'].values), 'low': list(data['Low'].values),'close': list(data['Close'].values), 'open': list(data['Open'].values),'name': stock_name.split('%')[1], 'upline': value2, 'downline': value1, 'upline_time':linedata2, 'downline_time':linedata1})
        
