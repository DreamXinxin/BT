# -*- coding:utf-8 -*-
__author__ = 'xin'
import talib
import numpy as np


class Demo(object):
    def __init__(self):
        pass

    def main(self, data):
        for i in range(len(data)):
            symbol = 'BTCUSD'
            price = data[i]
            date_time = data.index[i]
            ########策略逻辑#########
            flag_1 = 0  # 满足 开仓信号
            flag_2 = 1  # 满足 平仓信号
            ########################
            if flag_1 == 0:
                info_dict = {}
                info_dict['symbol'] = symbol
                info_dict['price'] = price
                info_dict['datetime'] = date_time
                info_dict['vol'] = ''
                info_dict['type'] = '_open'
                return info_dict
            elif flag_2 == 0:
                info_dict = {}
                info_dict['symbol'] = symbol
                info_dict['price'] = price
                info_dict['datetime'] = date_time
                info_dict['vol'] = ''
                info_dict['type'] = '_close'
                return info_dict

            else:
                return {}

    def run(self, info_d):
        price = info_d['price']          # 当时时间点对应的价格
        date_time = info_d['datetime']   # 时间点
        dataLen = info_d['dataLen']      # 总数据中遍历到 哪部分的长度
        data = info_d['data']            # 回测周期全部数据

        ################################ 编写自己的交易策略 ##########################################

        # 使用的技术指标
        MA = talib.MA(np.array(data), timeperiod=10)

        # 开仓信号  满足开仓信号 将flag 赋值为1 返回
        if data[dataLen] > MA[dataLen]:                  # 条件语句作为策略开仓信号  自己可更改
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
