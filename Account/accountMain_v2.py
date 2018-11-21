# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
__author__ = 'xin'

"""
此文件是创建虚拟账户 
"""
from Data.dataMain import HistoryData
import talib
import numpy as np
from collections import OrderedDict
import datetime
from Strategy.strategy1 import Demo


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
    def __init__(self, arg):
        self.arg = arg
        self.symbol = symbol_history_list                          # symbol list
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

        self.csv_time_list = []
        self.csv_balance_list = []
        self.csv_openPrice_list = []
        self.csv_closePrice_list = []
        self.csv_dataPrice_list = []

        self.zhibiao = None


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
    def handle_data(self, data_dict=None, today=None, price_type=None):
        data = data_dict[list(data_dict.keys())[0]]
        print('处理数据为:', data.columns[-1])
        real_data = data
        data = data[data.columns[-1]]
        demo = Demo(self.arg)

        for i in range(len(data)):
            # print('data[i], a[i]', data[i], a[i])
            today = real_data.index[i]
            try:
                price = data[i + 1]
            except:
                price = np.nan

            info_d = {}
            info_d['datetime'] = today
            info_d['price'] = price
            info_d['data'] = data
            info_d['dataLen'] = i                  # 记入数据长度

            # 获取开平仓信号
            info = demo.run(info_d)
            # if data[i] > a[i] and self.openFlag == True:
            if info['status'] == 'open':
                print('建仓 -- 价格{}--方向{}'.format(data[i], info['side']))
                # TODO 做交易 下单
                # XXXXXXXXXX
                print('时间挫{}'.format(today))
                print('allowSell_symbol:', self.allowSell_symbol)
                for j in self.symbol:
                    self.order_buy(j, 1, price=data[i], date_time=today, type='market', side=info['side'])
                    self.every_handle_BuyBalance(i, 1, price=data[i])

                #######################
                self.csv_openPrice_list.append(data[i])
                self.csv_closePrice_list.append('')
                self.csv_dataPrice_list.append(data[i])


            # elif data[i] < a[i] and self.sellFlag == True:
            elif info['status'] == 'close' :
                print('平仓 -- 价格{}--方向{}'.format(data[i], info['side']))
                print('时间挫{}'.format(today))
                print('allowSell_symbol:', self.allowSell_symbol)
                # TODO 做交易 下单
                # XXXXXXXXXX
                for k in self.symbol:
                    self.order_sell(k, 1, price=data[i], date_time=today, type='market', side=info['side'])
                    self.every_handle_SellBalance(i, 1, price=data[i])

                self.csv_openPrice_list.append('')
                self.csv_closePrice_list.append(data[i])
                self.csv_dataPrice_list.append(data[i])

            else:
                print('不开仓--时间挫{}--当前价格{}'.format(today, price))
                print('allowSell_symbol:', self.allowSell_symbol)
                # self.every_handle_Balance(price=price)
                self.csv_openPrice_list.append('')
                self.csv_closePrice_list.append('')
                self.csv_dataPrice_list.append(data[i])

                pass
            print('当前余额{}'.format(self.balance))
            self.csv_balance_list.append(self.balance)
            self.csv_time_list.append(today)

        self.every_balance.append(self.balance)
        print('balance 列表', self.every_balance)
        self.free_cash_list.append(self.free_cash)
        self.used_cash_list.append(self.used_cash)
        print(self.allowSell_symbol)
        self.MA = demo.MA


    # 信号 建仓
    def order_buy(self, symbol, amount, price, type, date_time, side):
        print('建仓交易')
        self.Order(symbol, amount, price)
        order_info = {}
        order_info['symbol'] = symbol
        order_info['amount'] = amount
        order_info['price'] = price
        order_info['type'] = type
        order_info['side'] = side
        self.allowSell_symbol[str(date_time)] = order_info
        self.trade_date.append(date_time)
        pass

    # 信号 平仓
    def order_sell(self, symbol, amount, price, type, date_time,side):
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
        l = []
        for i in self.allowSell_symbol:
            self.used_cash -= float(self.allowSell_symbol[i]['price'])
            cash = float(self.allowSell_symbol[i]['amount']) * float(self.allowSell_symbol[i]['price'])*(1 - self.close_fee)
            print('扣除平仓手续后，退还金额:{}'.format(cash))
            # 利润计算
            if self.allowSell_symbol[i]['side'] == 'buy':
                profit = (float(price) - float(self.allowSell_symbol[i]['price'])) * float(self.allowSell_symbol[i]['amount'])
            else:
                profit = -1 * (float(price) - float(self.allowSell_symbol[i]['price'])) * float(self.allowSell_symbol[i]['amount'])

            print('获得利润为{}'.format(profit))
            self.balance += profit
            self.free_cash = self.balance - self.used_cash

            l.append(i)
        for j in l:
            del self.allowSell_symbol[j]

        print('退还后的总余额：{}'.format(self.balance))
        # self.every_balance.append(self.balance)

    # 不下单子时处理 余额
    def every_handle_Balance(self, price):
        # self.every_balance.append(self.balance)
        for i in self.allowSell_symbol:
            if self.allowSell_symbol[i]['side'] == 'buy':
                profit = (float(price) - float(self.allowSell_symbol[i]['price'])) * float(self.allowSell_symbol[i]['amount'])
            else:
                profit = -1 * (float(price) - float(self.allowSell_symbol[i]['price'])) * float(self.allowSell_symbol[i]['amount'])

            self.balance += profit
            print('持仓中余额', self.balance)
        pass

    # TODO 策略入口函数
    def strategy(self, data):

        pass


if __name__ == '__main__':
    # Account().get_history('a', 'a', 'a', 'a')
    # l_data = [1.0, 2.0, 3.0, 4.0, 5.0]
    # a = talib.MA(np.array(l_data), timeperiod=5)
    Account().handle_data()










