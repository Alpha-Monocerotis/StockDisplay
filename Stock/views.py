from django.shortcuts import render
from django.http import *
from Stock.plot.plotStock import generate
# Create your views here.
from django.views.generic.base import View
import pandas as pd
from .models import Stock

ADDED = '''<form method="post" action="/stock">
            <label>
            股票名称
            </label>
             <select name="stock-name" id="stock-id">
                <option value ="请选择">请选择</option>
                {% for stock in stocks %}
                <option value ={{ stock.file }}>{{ stock.name }}</option>
                {% endfor %}
             </select>
            <div class="text-center" style="margin-top: 20px">
            <button type="submit">
                生成
            </button>
            </div>
            </form>'''

stock_data = pd.read_csv('Stock/data/stocks.csv', encoding='gb18030', header=None)


class Refresh_page(View):

    @staticmethod
    def get(req: HttpRequest):
        with open('templates/sample.html', mode='r') as f:
            splited = f.read().split(
                '''style="width:2000px;height:600px;"></div>
    <script type="text/javascript">''')
            head_and_plot = splited[0] + '''style="width:2000px;height:600px;"></div>'''
            tail = '<script type="text/javascript">' + splited[1]
        with open('templates/samples.html', mode='w') as f:
            f.write(head_and_plot + ADDED + tail)

        stocks = []
        for i in range(len(stock_data)):
            newStock = Stock()
            newStock.name = stock_data[3].values[i]
            newStock.file = 'Stock' + stock_data[7].values[i][1:]
            stocks.append(newStock)

        # stocks = [newStock]
        return render(req, 'samples.html', {'stocks': stocks})

    @staticmethod
    def post(req: HttpRequest):
        stock_name = req.POST['stock-name']

        generate(stock_name)
        with open('templates/sample.html', mode='r') as f:
            splited = f.read().split(
                '''style="width:2000px;height:600px;"></div>
    <script type="text/javascript">''')
            head_and_plot = splited[0] + '''style="width:2000px;height:600px;"></div>'''
            tail = '<script type="text/javascript">' + splited[1]
        with open('templates/samples.html', mode='w') as f:
            f.write(head_and_plot + ADDED + tail)
        stocks = []
        for i in range(len(stock_data)):
            newStock = Stock()
            newStock.name = stock_data[3].values[i]
            newStock.file = 'Stock' + stock_data[7].values[i][1:]
            stocks.append(newStock)
        return render(req, 'samples.html', {'stocks': stocks})
