from django.shortcuts import render
from django.http import *
# from Stock.plot.plotStock import generate
# Create your views here.
from django.views.generic.base import View
from time import localtime
import pandas as pd
from .models import Stock
from .plot.plotStock import zheline
__all__ = ['stock_name_list', 'TEST_PATH']
stock_name_list = pd.read_csv('Stock/data/stocks.csv', encoding='gb18030', header=None)
# Get stock name and filepath list from csv file.
TEST_PATH = "Stock/data/SH/SH000001.csv"
# TEST_PATH is for testing.


def compare_date(date1: str, date2: str):
    date1_year = date1.split('-')[0]
    date2_year = date2.split('-')[0]
    date1_month = date1.split('-')[1]
    date2_month = date2.split('-')[1]
    if int(date1_year) < int(date2_year):
        return True
    elif int(date1_year) > int(date2_year):
        return False
    else:  #
        if int(date1_month) <= int(date2_month):  #
            return True
        else:
            return False

class Refresh_page(View):
    @staticmethod
    def get(req: HttpRequest):
        stocks = []
        for i in range(len(stock_name_list)):
            newStock = Stock()
            newStock.name = stock_name_list[3].values[i]
            newStock.file = 'Stock' + stock_name_list[7].values[i][1:] + '%' + newStock.name
            stocks.append(newStock)
        now_year = localtime()[0]
        scopes = []
        for i in range(2000, now_year + 1):
            for j in range(1, 13):
                if j < 10:
                    scopes.append(str(i) + '-0' + str(j))
                else:
                    scopes.append(str(i) + '-' + str(j))
        return render(req, 'index.html', {'stocks': stocks, 'scopes': scopes})



    @staticmethod
    def post(req: HttpRequest):
        stock_name = req.POST['stock-name']
        data = pd.read_csv(TEST_PATH)
        view_scope_start = req.POST['scope-start']
        view_scope_end = req.POST['scope-end']
        for i in range(1, 10):
            data['Date'] = data['Date'].str.replace('-' + str(i) + '-', '-0' + str(i) + '-', regex=True)
        print(data.Date)
        print(view_scope_end)
        if view_scope_end < view_scope_start:
            tmp = view_scope_end
            view_scope_end = view_scope_start
            view_scope_start = tmp
        elif view_scope_start == view_scope_end:
            raise BaseException("You appoint a very cramped scope which may be meaningless!")
        data = data[data.Date > view_scope_start]
        data = data[data.Date < view_scope_end]
        linedata1, value1, linedata2, value2 = zheline(high_value=data['High'].values, low_value=data['Low'].values, datetime=data['Date'].values)
        return JsonResponse(data={'status': 'success', 'date': list(data['Date'].values),'high': list(data['High'].values), 'low': list(data['Low'].values),'close': list(data['Close'].values), 'open': list(data['Open'].values),'name': stock_name.split('%')[1], 'upline': value2, 'downline': value1, 'upline_time':linedata2, 'downline_time':linedata1})
<<<<<<< HEAD
        
=======



>>>>>>> c4f78c45fbe4db84a3464fbcce12443777194b0b
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
        Examples:
            None
        """
        stock_name = req.POST['stock-name']
        view_scope_start = req.POST['scope-start']
        view_scope_end = req.POST['scope-end']
        stock_data = pd.read_csv(stock_name.split('%')[0])
        stock_data = stock_data[stock_data.date > view_scope_start]
        data = stock_data[stock_data.date < view_scope_end]
        linedata1, value1, linedata2, value2 = zheline(high_value=data['High'].values,low_value=data['Low'].values, datetime=data['Date'].values)
        return JsonResponse(data={'status': 'success', 'date': list(data['Date'].values),'high': list(data['High'].values), 'low': list(data['Low'].values),'close': list(data['Close'].values), 'open': list(data['Open'].values),'name': stock_name.split('%')[1], 'upline': value2, 'downline': value1, 'upline_time':linedata2, 'downline_time':linedata1})
        
