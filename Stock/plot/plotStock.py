# -- coding:utf-8 --
import pandas as pd
from Stock.plot.getencoding import get_encoding
from pyecharts import Line, Kline, Overlap
# font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=12)

# filepath='./data/SH000001.csv'


# filepath = './data/000001d.csv'

df = None
resultdata = None
HighValue = None
closeValue = None
openValue = None
lowValue = None
time = None




def plotline():
    line = Line(u"上证指数", width=2000, height=600, is_animation=True)
    line.add("五分线", time, HighValue, is_label_show=True, is_datazoom_show=True, datazoom_extra_type="both",
             # TODO 额外缩放条配置
             is_datazoom_extra_show=True,  # 是否开启额外的缩放条
             datazoom_extra_orient="horizontal",  # 默认纵向
             xaxis_name="时间",
             tooltip_trigger="axis",
             # 触发类型，item=数据项触发，默认，主要在散点图，饼图等无类目图中使用，xais=坐标轴触发，主要在柱状图，折线图等有类目的途中使用，none=什么都不触发
             tooltip_trigger_on="mousemove|click",
             # 触发条件,
             # mousemove=鼠标移动的时候，click=点击的时候，mousemove|click=点击或移动的时候，none=不触发
             tooltip_axispointer_type="cross",  # 指示器类型，默认=line，直线，shadow=隐形，cross=十字准星
             tooltip_formatter='{c}',
             # str类型，{a}=系列名称add第一个参数，{b}=对应的x轴值，{c}=x,y坐标
             tooltip_text_color="red",  # 提示框文本的颜色
             tooltip_font_size=12,  # 提示框字体的大小
             tooltip_background_color="pink",  # 提示框背景色
             # tooltip_border_color="green",  # 提示框边框的颜色
             # tooltip_border_width=10,  # 边框的宽度
             )
    line.render("/Users/lmy/PycharmProjects/StockDisplay/templates/sample.html")


def PlotKline():
    kline = Kline()
    kline.add("五分k线", time, resultdata.values[:, 1:5], is_datazoom_show=True, datazoom_extra_type="both",
              # TODO 额外缩放条配置
              is_datazoom_extra_show=True,  # 是否开启额外的缩放条
              datazoom_extra_orient="horizontal",  # 默认纵向
              xaxis_name="时间",
              tooltip_trigger="axis",
              # 触发类型，item=数据项触发，默认，主要在散点图，饼图等无类目图中使用，xais=坐标轴触发，主要在柱状图，折线图等有类目的途中使用，none=什么都不触发
              tooltip_trigger_on="mousemove|click",
              # 触发条件,
              # mousemove=鼠标移动的时候，click=点击的时候，mousemove|click=点击或移动的时候，none=不触发
              tooltip_axispointer_type="cross",  # 指示器类型，默认=line，直线，shadow=隐形，cross=十字准星
              tooltip_formatter='{c}',
              # str类型，{a}=系列名称add第一个参数，{b}=对应的x轴值，{c}=x,y坐标
              tooltip_text_color="red",  # 提示框文本的颜色
              tooltip_font_size=12,  # 提示框字体的大小
              tooltip_background_color="pink",  # 提示框背景色
              )
    line = Line()
    line.add("五分线", time, HighValue)
    overlap = Overlap(u"五分k线", width=2000, height=600)
    overlap.add(kline)
    overlap.add(line,)
    overlap.add(zheline())
    overlap.render("kline.html")


def CKline(rejectdot=3):
    kdata = list()
    kdatas = list()
    flag = 0  # 0下降 ，1表示上升
    for i in range(len(HighValue) - 1):
        if(flag == 0):
            kdata.append(i)
            # if(HighValue[i+1]>HighValue[i] and len(kdata)>2 and
            # closeValue[i+1]> [i]):
            if (HighValue[i + 1] > HighValue[i]):
                if(len(kdata) > rejectdot):
                    if(len(kdatas) > 2 and kdatas[len(kdatas) - 2] == 0):
                        kdatas[len(kdatas) -
                               1] = kdatas[len(kdatas) - 1] + kdata
                    else:
                        kdatas.append(flag)
                        kdatas.append(kdata)
                    kdata = list()
                    flag = 1
                else:
                    if(HighValue[kdata[0]] < HighValue[i + 1]):
                        flag = 1
                    i = i + 1
                kdata.append(i)
        if(flag == 1):
            kdata.append(i)
            # if(HighValue[i+1]<HighValue[i] and len(kdata)>2 and
            # closeValue[i+1]<closeValue[i]):
            if (HighValue[i + 1] < HighValue[i]):
                if (len(kdata) > rejectdot):
                    if (len(kdatas) > 2 and kdatas[len(kdatas) - 2] == 1):
                        kdatas[len(kdatas) -
                               1] = kdatas[len(kdatas) - 1] + kdata
                    else:
                        kdatas.append(flag)
                        kdatas.append(kdata)
                    kdata = list()
                    flag = 0
                else:
                    if (HighValue[kdata[0]] > HighValue[i + 1]):
                        flag = 0
                    i = i + 1
                kdata.append(i)
    return kdatas


def zheline():
    dataline = CKline()
    line1data = list()
    line2data = list()
    value1 = list()
    value2 = list()
    for i in range(len(dataline) - 1):
        if(dataline[i] == 0):
            line1data.append(dataline[i + 1][0])
            line1data.append(dataline[i + 1][len(dataline[i + 1]) - 1])
            value1.append(HighValue[dataline[i + 1][0]])
            value1.append(lowValue[dataline[i + 1][len(dataline[i + 1]) - 1]])
            for v in dataline[i + 1]:
                value2.append(None)
                line2data.append(v)
        if (dataline[i] == 1):
            line2data.append(dataline[i + 1][0])
            line2data.append(dataline[i + 1][len(dataline[i + 1]) - 1])
            value2.append(lowValue[dataline[i + 1][0]])
            value2.append(HighValue[dataline[i + 1][len(dataline[i + 1]) - 1]])
            for v in dataline[i + 1]:
                value1.append(None)
                line1data.append(v)
    line = Line("五分笔线")
    line.add(
        "五分笔线",
        line1data,
        value1,
        line_color='black',
        line_width=2,
        is_connect_nones=False)
    line.add(
        "五分笔线",
        line2data,
        value2,
        line_color='blue',
        line_width=2,
        is_connect_nones=False)
    return line

def generate(filepath):
    global df
    df = pd.read_csv(
    filepath,
    iterator=True,
    encoding=get_encoding(filepath))

    global resultdata
    global HighValue
    global closeValue
    global openValue
    global lowValue
    global time
    resultdata = df.get_chunk()
    HighValue = resultdata.values[:, 4]
    closeValue = resultdata.values[:, 2]
    openValue = resultdata.values[:, 1]
    lowValue = resultdata.values[:, 3]
    time = resultdata.values[:, 0]
    plotline()

if __name__ == '__main__':
    # result=CKline()
    filepath = '/Users/lmy/PycharmProjects/StockDisplay/Stock/plot/SH000001.csv'
    generate(filepath)
    print('Run End')
