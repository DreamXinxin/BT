# -*- coding:utf-8 -*-
__author__ = 'xin'
import talib
import numpy as np


class Demo(object):
    def __init__(self, arg):
        self.arg = arg
        self.buyflag = 0
        self.sellflag = 0

        pass

    def run(self, info_d):
        price = info_d['price']          # 当时时间点对应的价格
        date_time = info_d['datetime']   # 时间点
        dataLen = info_d['dataLen']      # 总数据中遍历到 哪部分的长度
        data_dict = info_d['data']            # 回测周期全部数据
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
        ################################ 编写自己的交易策略 ##########################################

        # 使用的技术指标
        MA = talib.MA(np.array(data), timeperiod=self.arg)
        self.MA = MA
        if data[dataLen] > MA[dataLen] and self.buyflag == 0 and self.sellflag == 0:
            info = {}
            info['price'] = price
            info['side'] = 'buy'
            info['status'] = 'open'
            self.buyflag = 1
            return info
        elif data[dataLen] < MA[dataLen] and self.buyflag == 1:
            info = {}
            info['price'] = price
            info['side'] = 'buy'
            info['status'] = 'close'
            self.buyflag = 0
            return info

        elif data[dataLen] < MA[dataLen] and self.sellflag == 0 and self.buyflag == 0:
            info = {}
            info['price'] = price
            info['side'] = 'sell'
            info['status'] = 'open'
            self.sellflag = 1
            return info
        elif data[dataLen] > MA[dataLen] and self.sellflag == 1:
            info = {}
            info['price'] = price
            info['side'] = 'sell'
            info['status'] = 'close'
            self.sellflag = 0
            return info

        else:
            info = {}
            info['price'] = ''
            info['side'] = ''
            info['status'] = ''
            self.flag = 0
            return info




if __name__ == '__main__':
     Demo(10)
