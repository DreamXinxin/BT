# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
__author__ = 'xin'
import talib
import numpy as np


class Strategy(object):
    def __init__(self, account, strategy_arg):
        self.account = account
        self.strategy_arg = strategy_arg
        self.buyflag = 0
        self.sellflag = 0

    def get_accountInfo(self):
        pass

    # 查询订单功能
    def get_history_orders(self):
        return self.account.get_user_history_orders()

    def get_signal(self, info_dict):
        """

        :param info_dict['before_data'] : 数据结构是 Dataframe 
                                            2017-07-01 00:00:00  2420.700000
                                            2017-07-01 01:00:00  2424.700000
                                            2017-07-01 02:00:00  2383.200000
                                            2017-07-01 03:00:00  2378.900000

        
        :return: 
        """
        # 基础信息
        data_df = info_dict['before_data']                    # 当前之前的历史数据 数据结构是 Dataframe
        data_list = list(data_df[data_df.columns[0]] )       # 当前时刻数据  数据结构是 list
        dataLen = info_dict['dataLen']                      # 当前索引
        price = data_df[data_df.columns[0]][dataLen]       # 当前时刻的价格
        # print('当前时刻价格', price)

        MA = talib.MA(np.array(data_df[data_df.columns[0]]), timeperiod=self.strategy_arg)
        self.MA = MA
        if data_list[dataLen] > MA[dataLen] and self.buyflag == 0 and self.sellflag == 0:
            info = {}
            info['price'] = price
            info['side'] = 'buy'
            info['status'] = 'open'
            info['type'] = 'market'
            info['amount'] = '1'
            self.buyflag = 1
            return info

        elif data_list[dataLen] < MA[dataLen] and self.buyflag == 1:
            info = {}
            info['price'] = price
            info['side'] = 'buy'
            info['status'] = 'close'
            info['type'] = 'market'
            info['amount'] = '1'
            self.buyflag = 0

            return info

        elif data_list[dataLen] < MA[dataLen] and self.sellflag == 0 and self.buyflag == 0:
            info = {}
            info['price'] = price
            info['side'] = 'sell'
            info['status'] = 'open'
            info['type'] = 'market'
            info['amount'] = '1'
            self.sellflag = 1
            return info
        elif data_list[dataLen] > MA[dataLen] and self.sellflag == 1:
            info = {}
            info['price'] = price
            info['side'] = 'sell'
            info['status'] = 'close'
            info['type'] = 'market'
            info['amount'] = '1'
            self.sellflag = 0
            return info

        else:
            info = {}
            # info['price'] = ''
            # info['side'] = ''
            # info['status'] = ''
            # self.flag = 0
            self.get_history_orders()
            return info

        pass


if __name__ == '__main__':
     pass
