# -*- coding:utf-8 -*-
__author__ = 'xin'
import talib
import numpy as np


class Demo(object):
    def __init__(self):
        pass

    def run(self, info_d):
        price = info_d['price']          # 当时时间点对应的价格
        date_time = info_d['datetime']   # 时间点
        dataLen = info_d['dataLen']      # 总数据中遍历到 哪部分的长度
        data_dict = info_d['data_dict']            # 回测周期全部数据

        for symbol,symbol_data in data_dict.items():
            print(symbol)

        # ############################### 编写自己的交易策略 ##########################################
        # data = data_dict[list(data_dict.keys())[0]]
        try:
            data = data_dict[list(data_dict.keys())[0]]['close']
        except:
            try:
                data = data_dict[list(data_dict.keys())[0]]['open']
            except:
                try:
                    data = data_dict[list(data_dict.keys())[0]]['high']
                except:
                    data = data_dict[list(data_dict.keys())[0]]['low']

        # 使用的技术指标
        MA = talib.MA(np.array(data), timeperiod=10)

        # 开仓信号  满足开仓信号 将flag 赋值为1 返回
        if data[dataLen] > MA[dataLen]:                  # 条件语句作为策略开仓信号  自己可更改

            # TODO 返回的数据 字典  price vol datetime
            flag = 1
            return flag
        # 平仓信号
        elif data[dataLen] < MA[dataLen]:                # # 条件语句作为策略开仓信号  自己可更改
            flag = -1
            return flag
        else:
            flag = 0
            return flag


if __name__ == '__main__':
     Demo()
