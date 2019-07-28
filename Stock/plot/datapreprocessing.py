import os

import pandas as pd

from matplotlib.font_manager import FontProperties
from Stock.plot.getencoding import get_encoding
# import getencoding
font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=12)


def stocklist():
    filepath = './data/stockcode.csv'
    savefilepath = './data/stocks.csv'
    df = pd.read_csv(filepath, encoding='gb18030')  # 读入股票数据
    # dataframe.iloc即按位置选择数据，即第n行，第n列数据,取第3-10列,.values把Pandas中的dataframe转成numpy中的array
    data = df.values[:, 1]
    stock = list()
    address = ''
    file = open(savefilepath, 'w')
    for i in range(len(data)):
        codes = str(data[i]).split('.')
        if(codes[1] == 'SZ'):
            if(os.path.exists('./data/SZ/SZ' + str(codes[0]) + '.csv')):
                address = './data/SZ/SZ' + str(codes[0]) + '.csv'
            else:
                continue
        else:
            if (os.path.exists('./data/SH/SH' + str(codes[0]) + '.csv')):
                address = './data/SH/SH' + str(codes[0]) + '.csv'
            else:
                continue
        file.writelines(str(df.values[i, 0]) + ',' +
                        str(df.values[i, 1]) + ',' +
                        str(df.values[i, 2]) + ',' +
                        str(df.values[i, 3]) + ',' +
                        str(df.values[i, 4]) + ',' +
                        str(df.values[i, 5]) + ',' +
                        str(df.values[i, 6]) + ',' +
                        address)
        file.writelines('\n')
    file.close()


def ReadFile(filepath):
    df = pd.read_csv(filepath, iterator=True, encoding=get_encoding(filepath))
    order = ['Date', 'Open', 'Close', 'Low', 'High', 'Volume', 'Amount']
    # df=df[order]
    resultdata = df.get_chunk()
    resultdata = resultdata[order]
    return resultdata


def CKline(HighValue, rejectdot=3):
    kdata = list()
    kdatas = list()
    flag = 0  # 0下降 ，1表示上升
    for i in range(len(HighValue) - 1):
        if flag == 0:
            kdata.append(i)
            if HighValue[i + 1] > HighValue[i]:
                if len(kdata) > rejectdot:
                    if len(kdatas) > 2 and kdatas[len(kdatas) - 2] == 0:
                        kdatas[len(kdatas) -
                               1] = kdatas[len(kdatas) - 1] + kdata[1:]
                    else:
                        kdatas.append(flag)
                        kdatas.append(kdata)
                    kdata = list()
                    flag = 1
                else:
                    if HighValue[kdata[0]] < HighValue[i + 1]:
                        flag = 1
                    if i + 1 >= len(HighValue) - 1:
                        break
                    i = i + 1
                    kdata.append(i)
        if flag == 1:
            kdata.append(i)
            if HighValue[i + 1] < HighValue[i]:
                if (len(kdata) > rejectdot):
                    if len(kdatas) > 2 and kdatas[len(kdatas) - 2] == 1:
                        kdatas[len(kdatas) -
                               1] = kdatas[len(kdatas) - 1] + kdata[1:]
                    else:
                        kdatas.append(flag)
                        kdatas.append(kdata)
                    kdata = list()
                    flag = 0
                else:
                    if HighValue[kdata[0]] > HighValue[i + 1]:
                        flag = 0
                    if i + 1 >= len(HighValue) - 1:
                        break
                    i = i + 1
                    kdata.append(i)
    return kdatas


def gradient(filepath='./data/000001d.csv'):
    names = filepath.split('/')
    filepath = './data/' + names[len(names) - 2] + '/' + names[len(names) - 1]
    resultdata = ReadFile(filepath)
    # print(filepath)
    time = resultdata.values[:, 0]
    lowValue = resultdata.values[:, 3]
    HighValue = resultdata.values[:, 4]
    datas = CKline(3, HighValue)
    # names = filepath.split('/')
    # savefilepath = './data/gradient/SH' + names[len(names) - 1]
    savefilepath = './data/gradient1/' + \
        names[len(names) - 2] + '/' + names[len(names) - 1]
    file = open(savefilepath, 'w')
    file.writelines("time,low,high,length,gradient,orientation")
    file.writelines('\n')
    for i in range(len(datas)):
        if isinstance(datas[i], type(1)):
            continue
        d = datas[i]
        gd = list()
        gd.append(time[d[0]])
        gd.append(lowValue[d[0]])
        gd.append(HighValue[d[0]])
        gd.append(len(d))
        if datas[i - 1] == 0:
            gd.append(0 - (d[len(d) - 1] - d[0]) / float(len(d)))
        else:
            gd.append((d[len(d) - 1] - d[0]) / float(len(d)))
        file.writelines(str(gd[0]) +
                        "," +
                        str(gd[1]) +
                        "," +
                        str(gd[2]) +
                        "," +
                        str(gd[3]) +
                        "," +
                        str(gd[4]) +
                        "," +
                        str(datas[i -
                                  1]))
        file.writelines('\n')
    file.close()


if __name__ == '__main__':
    filepath = './data/stocks.csv'
