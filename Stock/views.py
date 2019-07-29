from django.shortcuts import render
from django.http import *
from django.views.generic.base import View
from time import localtime
import pandas as pd
from .models import Stock
from .plot.plotStock import zheline
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
        now_year = localtime()[0]
        scopes = []
        for i in range(2000, now_year + 1):
            for j in range(1, 13):
                if j < 10:
                    scopes.append(str(i) + '-0' + str(j))
                else:
                    scopes.append(str(i) + '-' + str(j))
                # Here we plus a 0 infront of every single month digit to resolve the dict index problem.
        return render(req, 'index.html', {'stocks': stocks, 'scopes': scopes})

    @staticmethod
    def post(req: HttpRequest):
        stock_name = req.POST['stock-name']
        data = pd.read_csv(TEST_PATH)
        # In a prodictive environment, you are supposed to use stock_name.split('%')[0] to replace the TEST_PATH
        view_scope_start = req.POST['scope-start']
        view_scope_end = req.POST['scope-end']
        for i in range(1, 10):
            data['Date'] = data['Date'].str.replace('-' + str(i) + '-', '-0' + str(i) + '-', regex=True)
        if view_scope_end < view_scope_start:
            tmp = view_scope_end
            view_scope_end = view_scope_start
            view_scope_start = tmp
        elif view_scope_start == view_scope_end:
            raise BaseException("You appoint a very cramped scope which may be meaningless!")
            # We don't allow users to specify a scope whose start is the same as the end.
        data = data[data.Date > view_scope_start]
        data = data[data.Date < view_scope_end]
        linedata1, value1, linedata2, value2 = zheline(high_value=data['High'].values, low_value=data['Low'].values, datetime=data['Date'].values)
        return JsonResponse(data={'status': 'success', 'date': list(data['Date'].values),'high': list(data['High'].values), 'low': list(data['Low'].values),'close': list(data['Close'].values), 'open': list(data['Open'].values),'name': stock_name.split('%')[1], 'upline': value2, 'downline': value1, 'upline_time':linedata2, 'downline_time':linedata1})
        
