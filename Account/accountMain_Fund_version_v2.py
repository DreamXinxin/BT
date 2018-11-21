# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
__author__ = 'xin'

"""
此文件是创建虚拟账户 
"""
from Data.dataMain_Fund_version import HistoryData
import talib
import numpy as np
from collections import OrderedDict
import datetime
from Strategy.strategy1_Fund_version_v2 import Demo
import copy
from Setting.setting import start_date, end_date, init_dict, symbol_history_list, STRATEGY_NAME



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
    def __init__(self, init_dict, ):
        self.init_dict = init_dict
        self.symbol = ['BTC/USDT']                             # symbol list
        self.cash = init_dict                           # 初始金额
        self.balance = init_dict                         # 账户余额
        self.free_cash = init_dict                      # 可使用资金
        self.free_cash_list = []
        self.used_cash = {}                      # 已用资金  使用的保证金
        self.used_cash_list = []
        self.allowClose_symbol = {}        # 可卖标的
        self.trade_date = []                         # 交易日日期
        self.back_test_date = []                     # 回测日期
        self.every_balance = []                      # 每日净值
        self.openFlag = True                         # 是否可以开仓标记
        self.closeFlag = False                        # 是否可以平仓
        self.limit_openFlag = True
        self.limit_closeFlag = False
        self.Order = Order                          # 下单模块
        self.blotter = []                            # 下单列表

        self.open_fee = 0.001                          # 开仓手续费
        self.close_fee = 0.001                         # 平仓手续费

        self.csv_time_list = []
        self.csv_balance_list = []
        self.csv_openPrice_dict = OrderedDict()                   # 记录建仓价格
        self.csv_closePrice_dict = OrderedDict()                 # 记录平仓价格
        self.csv_dataPrice_dict = OrderedDict()                 # 记录货币价格

        for i in init_dict:
            self.used_cash[i] = 0.0               # 初始化
        for i in symbol_history_list:
            self.csv_openPrice_dict[i] = []
            self.csv_closePrice_dict[i] = []
            self.csv_dataPrice_dict[i] = []

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
        # data = [float(x) for x in range(20)]
        # 获取时间长度搓 取数据字典中 第一个key 作为 后边遍历的标准
        data = data_dict[list(data_dict.keys())[0]]

        print('处理数据为:', data.columns[-1])
        real_data = data
        data = data[data.columns[-1]]

        # 创建策略实例
        demo = Demo()

        # a = talib.MA(np.array(data), timeperiod=10)
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
            info_d['data_dict'] = data_dict
            info_d['dataLen'] = i                  # 记入数据长度

            # 获取开平仓信号
            info_dict = demo.run(info_d)
            # if data[i] > a[i] and self.openFlag == True:
            print('\n时间挫{} \n'.format(today))

            # 判断是否有删除的挂单
            for d_index in range(len(demo.limit_order_list)):
                if demo.limit_order_list[d_index]['id'] == info_dict['delLimit']:
                    del demo.limit_order_list[d_index]

            for limit_order in demo.limit_order_list:
                if limit_order['side'] == 'buy':
                    if price < limit_order['openClose'] and self.limit_openFlag == True:
                        self.order_open(limit_order)
                        limit_order['status'] = True
                        self.limit_closeFlag = True
                        self.limit_openFlag = False
                        demo.limit_order_list.remove(limit_order)

                    if limit_order['status'] == True and self.limit_closeFlag == True:
                        self.order_close(limit_order)
                        self.limit_openFlag = True
                        self.limit_closeFlag = False
                        demo.limit_order_list.remove(limit_order)

                elif limit_order['side'] == 'sell' and self.limit_openFlag == True:
                    if price > limit_order['openClose']:
                        self.order_open(limit_order)
                        limit_order['status'] = True
                        self.limit_closeFlag = True
                        self.limit_openFlag = False
                        demo.limit_order_list.remove(limit_order)

                    if limit_order['status'] == True and self.limit_closeFlag == True:
                        self.order_close(limit_order)
                        self.limit_openFlag = True
                        self.limit_closeFlag = False
                        demo.limit_order_list.remove(limit_order)
                else:
                    pass


            # 遍历需要交易池
            # 如果是 市价单
            for market_open_order in demo.market_open_order_list:
                if self.openFlag == True:
                    self.order_open(market_open_order)
                    self.closeFlag = True
                    self.openFlag = False
            for market_close_order in demo.market_close_order_list:
                if self.closeFlag == True:
                    self.order_close(market_close_order)
                    self.openFlag = True
                    self.closeFlag = False
            for _k in data_dict.keys():
                self.csv_dataPrice_dict[_k] = data_dict[_k]


            l_balance = {}
            l_balance = copy.deepcopy(self.balance)
            print('当前余额{}'.format(l_balance))
            self.csv_balance_list.append(l_balance)
            self.csv_time_list.append(today)

            self.every_balance.append(l_balance)
            print('every_balance 列表', self.every_balance)
            print('csv_balance_list:', self.csv_balance_list)

            self.free_cash_list.append(self.free_cash)
            self.used_cash_list.append(self.used_cash)

            print('allowClose_symbol:', self.allowClose_symbol)

    # 信号 建仓
    def order_open(self, info_dict):
        print('建仓交易')
        # self.Order(symbol, amount, price)
        order_info = {}
        order_info['symbol'] = info_dict['symbol']
        order_info['amount'] = info_dict['amount']
        order_info['price'] = info_dict['openPrice']
        order_info['type'] = info_dict['type']
        order_info['datetime'] = info_dict['datetime']

        self.allowClose_symbol[info_dict['id']] = order_info
        self.trade_date.append(order_info['datetime'])
        self.every_handle_OpenBalance(info_dict)
        pass

    # 信号 平仓
    def order_close(self, info_dict):
        print('平仓交易')
        order_info = {}
        order_info['symbol'] = info_dict['symbol']
        order_info['amount'] = info_dict['amount']
        order_info['price'] = info_dict['closePrice']
        order_info['type'] = info_dict['type']
        order_info['datetime'] = info_dict['datetime']
        # self.Order(symbol, amount, price)
        self.trade_date.append(order_info['datetime'])
        self.every_handle_CloseBalance(info_dict)

        pass

    # 每日处理 建仓单
    def every_handle_OpenBalance(self, info_dict):
        price = float(info_dict['price'])
        amount = float(info_dict['amount'])
        order_amount = price * amount             # 需要下单的手数

        balance_coin = info_dict['balanceCoin']

        if self.free_cash[balance_coin] <= order_amount:
            print('金额不足无法交易, 当前可用金额为{}， 需要交易金额{}'.format(self.free_cash[balance_coin], order_amount))
            pass
        else:
            self.used_cash[balance_coin] += float(amount * price)
            print('占用保证金为{}'.format(self.used_cash[balance_coin]))
            self.free_cash[balance_coin] = self.balance[balance_coin] - self.used_cash[balance_coin]
            self.balance[balance_coin] = self.balance[balance_coin] - float(amount * price)* self.open_fee
            # self.every_balance.append(self.balance)
            print('扣除开仓手续费{}'.format(float(amount * price)* self.open_fee))
            print('下单之后当前可用金额:{}'.format(self.free_cash[balance_coin]))

    # 每日处理 平仓单
    def every_handle_CloseBalance(self, info_dict):
        # self.cash = self.cash - float(amount * price)
        price = float(info_dict['price'])
        amount = float(info_dict['amount'])
        order_amount = price * amount  # 需要下单的手数

        balance_coin = info_dict['balance_coin']

        for id in list(self.allowClose_symbol.keys()):
            self.used_cash[balance_coin] -= float(self.allowClose_symbol[id]['price'])
            cash = float(self.allowClose_symbol[id]['amount']) * float(self.allowClose_symbol[id]['price'])*(1 - self.close_fee)
            print('扣除平仓手续后，退还金额:{}'.format(cash))
            # 利润计算
            profit = (float(price) - float(self.allowClose_symbol[id]['price'])) * float(self.allowClose_symbol[id]['amount'])
            print('获得利润为{}'.format(profit))
            self.balance[balance_coin] += profit
            self.free_cash[balance_coin] = self.balance[balance_coin] - self.used_cash[balance_coin]

            del self.allowClose_symbol[id]

        print('退还后的总余额：{}'.format(self.balance[balance_coin]))
        # self.every_balance.append(self.balance)

    # 不下单子时处理 余额
    def every_handle_Balance(self, date_time):
        # self.every_balance.append(self.balance)
        pass

    # TODO 策略入口函数
    def strategy(self, data):

        pass


if __name__ == '__main__':
    # Account().get_history('a', 'a', 'a', 'a')
    # l_data = [1.0, 2.0, 3.0, 4.0, 5.0]
    # a = talib.MA(np.array(l_data), timeperiod=5)
    Account().handle_data()










