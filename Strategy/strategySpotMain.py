# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
__author__ = 'xin'
import talib
import numpy as np


class Strategy(object):
    def __init__(self, account, strategy_arg):
        self.account = account
        self.strategy_arg = strategy_arg
        # self.flag = 0
        self.buyflag = 0
        self.sellflag = 0
        self.num = 0

    def get_accountInfo(self):
        pass

    # 查询订单功能
    def get_history_orders(self):
        return self.account.get_user_history_orders()

    def get_id(self):
        self.num += 1
        return self.num

    # 撤单
    def del_order(self, id):
        for i in self.account.historyLimitOrder_list:
            if i['id'] == id:
                self.account.historyLimitOrder_list.remove(i)

    # 下单
    def order(self, symbol, price, amount, side, type):
        """
        
        :param symbol:   货币对
        :param price:    价格
        :param amount:   数量
        :param side:     buy or sell
        :param type:     market or limit
        :return:         dict 
        """
        info = {}
        info['id'] = self.get_id()
        info['symbol'] = symbol
        info['price'] = price
        info['side'] = side
        info['type'] = type
        info['amount'] = amount

        return info

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
        data_df = info_dict['before_data']  # 当前之前的历史数据 数据结构是 Dataframe
        data_list = list(data_df[data_df.columns[0]])  # 当前时刻数据  数据结构是 list
        dataLen = info_dict['dataLen']  # 当前索引
        price = data_df[data_df.columns[0]][dataLen]  # 当前时刻的价格
        # print('当前时刻价格', price)

        MA = talib.MA(np.array(data_df[data_df.columns[0]]), timeperiod=self.strategy_arg)
        self.MA = MA
        # print('\n此时价格差####{}--'.format(float(data_list[dataLen] - MA[dataLen])))
        # print('上一时刻差####{}--\n'.format(float(data_list[dataLen - 1] - data_list[dataLen - 1])))
        if data_list[dataLen] > MA[dataLen] and data_list[dataLen - 1] < MA[dataLen - 1]:
            # info = self.order('BTC/USD', price, 1, 'buy', 'market')
            info = self.order('BTCUSD', price, 1, 'buy', 'market')

            return info

        elif data_list[dataLen] < MA[dataLen] and data_list[dataLen - 1] > MA[dataLen - 1]:
            info = self.order(symbol='BTCUSD', price=price, amount=1, side='sell', type='market')
            return info

        else:
            info = {}
            return info

        pass


if __name__ == '__main__':
    pass
