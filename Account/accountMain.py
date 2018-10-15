# -*- coding:utf-8 -*-
__author__ = 'xin'

"""
此文件是创建虚拟账户 
"""
from BackTest_v1.Data.dataMain import HistoryData
import talib
import numpy as np
from collections import OrderedDict
import datetime


class Order(object):
    def __init__(self, symbol, amount, time=None, type='market', price=0.):
        self.order_time = ''          # 指令下达时间 datetime
        self.symbol = symbol          # 交易标的
        self.type = type              # 下单类型
        self.price = price            # 价格
        self.amount = amount          # 指令交易数量

        pass


class Account(object):
    # 初始化设置
    def __init__(self):
        self.symbol = ['BTC/USDT']                             # symbol list
        self.cash = 10000                            # 初始金额
        self.balance = 10000                         # 账户余额
        self.free_cash = 10000                      # 可使用资金
        self.free_cash_list = []
        self.used_cash = 0                       # 已用资金  使用的保证金
        self.used_cash_list = []
        self.allowSell_symbol = OrderedDict()        # 可卖标的
        self.trade_date = []                         # 交易日日期
        self.back_test_date = []                     # 回测日期
        self.every_balance = []                      # 每日净值
        self.openFlag = True                         # 是否可以开仓标记
        self.sellFlag = False                        # 是否可以平仓
        self.Order = Order                          # 下单模块
        self.blotter = []                            # 下单列表

        self.open_fee = 0.001                          # 开仓手续费
        self.close_fee = 0.001                         # 平仓手续费

        pass

    def get_history(self, symbol, start, end, freq):
        """
        获取历史数据
        :param symbol:           交易标的
        :param start:            起始时间
        :param end:              结束时间
        :param freq:             时间周期
        :return:                 { symbol : {closePrice:[ , , ,],
                                                     openPrice:[ , , ,],
                                                     highPrice:[ , , ,],
                                                                         }
        """
        return HistoryData().get_history_data()

    # 处理数据
    def handle_data(self, data=None, today=None, price_type=None):
        # data = [float(x) for x in range(20)]
        print('处理数据为:', data.columns[-1])
        real_data = data
        data = data[data.columns[-1]]
        print(data)
        a = talib.MA(np.array(data), timeperiod=10)
        for i in range(len(data)):
            # print('data[i], a[i]', data[i], a[i])
            today = real_data.index[i]
            if data[i] > a[i] and self.openFlag == True:
                print('建仓 -- 价格{}'.format(data[i]))
                # TODO 做交易 下单
                # XXXXXXXXXX
                print('时间挫{}'.format(today))
                for j in self.symbol:
                    self.order_buy(j, 1, price=data[i], date_time=today, type='market')
                    self.every_handle_BuyBalance(i, 1, price=data[i])
                #######################

                self.sellFlag = True
                self.openFlag = False
            elif data[i] < a[i] and self.sellFlag == True:
                print('平仓 -- 价格{}'.format(data[i]))
                print('时间挫{}'.format(today))
                # TODO 做交易 下单
                # XXXXXXXXXX
                for k in self.symbol:
                    self.order_sell(k, 1, price=data[i], date_time=today, type='market')
                    self.every_handle_SellBalance(i, 1, price=data[i])
                self.openFlag = True
                self.sellFlag = False
            else:
                self.every_handle_Balance(date_time=today)
                pass
            print('当前余额{}'.format(self.balance))
        self.every_balance.append(self.balance)
        print('balance 列表', self.every_balance)
        self.free_cash_list.append(self.free_cash)
        self.used_cash_list.append(self.used_cash)
        print(self.allowSell_symbol)

    # 信号 建仓
    def order_buy(self, symbol, amount, price, type, date_time):
        print('建仓交易')
        self.Order(symbol, amount, price)
        order_info = {}
        order_info['symbol'] = symbol
        order_info['amount'] = amount
        order_info['price'] = price
        order_info['type'] = type
        self.allowSell_symbol[str(date_time)] = order_info
        self.trade_date.append(date_time)
        pass

    # 信号 平仓
    def order_sell(self, symbol, amount, price, type, date_time):
        print('平仓交易')
        self.Order(symbol, amount, price)
        self.trade_date.append(date_time)

        pass

    # 每日处理 建仓单
    def every_handle_BuyBalance(self, symbol, amount, price):
        if self.free_cash <= price:
            print('金额不足无法交易, 当前可用金额为{}， 需要交易金额{}'.format(self.free_cash, price))
            pass
        else:
            self.used_cash += float(amount * price)
            print('占用保证金为{}'.format(self.used_cash))
            self.free_cash = self.balance - self.used_cash
            self.balance = self.balance - float(amount * price)* self.open_fee
            # self.every_balance.append(self.balance)
            print('扣除开仓手续费{}'.format(float(amount * price)* self.open_fee))
            print('下单之后当前可用金额:{}'.format(self.free_cash))

    # 每日处理 平仓单
    def every_handle_SellBalance(self, symbol, amount, price):
        # self.cash = self.cash - float(amount * price)
        print('allowSell_symbol:', self.allowSell_symbol)
        for i in self.allowSell_symbol:
            self.used_cash -= float(self.allowSell_symbol[i]['price'])
            cash = float(self.allowSell_symbol[i]['amount']) * float(self.allowSell_symbol[i]['price'])*(1 - self.close_fee)
            print('扣除平仓手续后，退还金额:{}'.format(cash))
            # 利润计算
            profit = (float(price) - float(self.allowSell_symbol[i]['price'])) * float(self.allowSell_symbol[i]['amount'])
            print('获得利润为{}'.format(profit))
            self.balance += profit
            self.free_cash = self.balance - self.used_cash

            del self.allowSell_symbol[i]

        print('退还后的总余额：{}'.format(self.balance))
        # self.every_balance.append(self.balance)

    # 不下单子时处理 余额
    def every_handle_Balance(self, date_time):
        # self.every_balance.append(self.balance)
        pass


if __name__ == '__main__':
    Account().get_history('a', 'a', 'a', 'a')
    l_data = [1.0, 2.0, 3.0, 4.0, 5.0]
    a = talib.MA(np.array(l_data), timeperiod=5)
    Account().handle_data()










