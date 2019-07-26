# -- coding:utf-8 --

import numpy as np
def CKline(high_value, rejectdot=3):
    kdata = list()
    kdatas = list()
    flag = 0
    for i in range(len(high_value) - 1):
        if (flag == 0):
            kdata.append(i)
            if (high_value[i + 1] > high_value[i]):
                if (len(kdata) > rejectdot):
                    if (len(kdatas) > 2 and kdatas[len(kdatas) - 2] == 0):
                            kdatas[len(kdatas) - 1] = kdatas[len(kdatas) - 1] + kdata[1:]
                    else:
                        kdatas.append(flag)
                        kdatas.append(kdata)
                    kdata = list()
                    flag = 1
                    kdata.append(i)
                else:
                    if (high_value[kdata[0]] < high_value[i + 1]):
                        flag = 1
        else:
            kdata.append(i)
            if (high_value[i + 1] < high_value[i]):
                if (len(kdata) > rejectdot):
                    if (len(kdatas) > 2 and kdatas[len(kdatas) - 2] == 1):
                        kdatas[len(kdatas) - 1] = kdatas[len(kdatas) - 1] + kdata[1:]
                    else:
                        kdatas.append(flag)
                        kdatas.append(kdata)
                    kdata = list()
                    flag = 0
                    kdata.append(i)
                else:
                    if (high_value[kdata[0]] > high_value[i + 1]):
                        flag = 0
    return kdatas

def zheline(high_value, low_value, datetime):
    dataline = CKline(high_value=high_value, rejectdot=3)
    # print(dataline)
    line1data = list()
    line2data = list()
    value1 = list()
    value2 = list()
    for i in range(len(dataline) - 1):
        if dataline[i] == 0:
            line1data.append(datetime[dataline[i + 1][0]])
            line1data.append(datetime[dataline[i + 1][len(dataline[i + 1]) - 1]])
            value1.append(high_value[dataline[i + 1][0]])
            value1.append(low_value[dataline[i + 1][len(dataline[i + 1]) - 1]])
            for v in dataline[i + 1]:
                value2.append(None)
                line2data.append(datetime[v])
        if dataline[i] == 1:
            line2data.append(datetime[dataline[i + 1][0]])
            line2data.append(datetime[dataline[i + 1][len(dataline[i + 1]) - 1]])
            value2.append(low_value[dataline[i + 1][0]])
            value2.append(high_value[dataline[i + 1][len(dataline[i + 1]) - 1]])
            for v in dataline[i + 1]:
                value1.append(None)
                line1data.append(datetime[v])
    return line1data, value1, line2data, value2


if __name__ == '__main__':
    high_value = np.array([1, 2, 3, 1, 2, 41, 7, 6, 1, 10, 11, 6, 13, 12, 15])
    print(zhe(high_value))
