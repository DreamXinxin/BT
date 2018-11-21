# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
__author__ = 'xin'

"""
此文件是创建虚拟账户 
"""
# from Data.dataMain import HistoryData
from pprint import pprint
import talib
import numpy as np
from collections import OrderedDict
import datetime
from Strategy.strategySpotMain import Strategy
import copy


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
    def __init__(self, init_dict, strategy_arg):
        self.strategy_arg = strategy_arg

        # TODO 多币种的时候 需要更改 目前已BTC作为结算
        self.symbol_list = init_dict['symbol_list']  # symbol list
        self.cash = copy.deepcopy(init_dict['cash'])               # 初始金额
        self.balance_dict = copy.deepcopy(init_dict['cash'])      # 账户余额
        self.btc_balance = []                                   # 记录btc变化余额
        self.free_cash = copy.deepcopy(init_dict['cash']['BTC'])    # 可使用资金
        self.today_symbol_price = {}                 # 记录当天价格
        self.firstday_symbol_price = {}                 # 记录第一天的价格
        self.end_balance = 0

        self.para_allowCash = 0                  # 在最后一天计算 策略 允许的最小容量
        self.allow_min_coin_dict = {}                    # 各个币种最近容量

        for symbol in init_dict['symbol_list']:
            self.today_symbol_price[symbol] = np.nan
            self.firstday_symbol_price[symbol] = np.nan

        self.historyOrder_list = []                  # 历史订单
        self.historyLimitOrder_list = []

        self.buy_fee = init_dict['fee']['buy_fee']                          # 开仓手续费
        self.sell_fee = init_dict['fee']['sell_fee']                         # 平仓手续费

        self.buy_openPrice_dict = {}
        self.sell_openPrice_dict = {}

        self.csv_time_list = []
        self.csv_signal_dict = {}
        self.csv_amount_dict = {}
        self.csv_balance_dict = {}
        self.csv_dataPrice_list = []

        for symbol in init_dict['cash']:
            self.csv_balance_dict[symbol] = []

    # 获取历史订单
    def get_user_history_orders(self):
        # print('获取历史订单', self.historyOrder_list)
        return self.historyOrder_list

    # 获取持仓单
    def get_user_orders(self):
        # TODO 返回历史订单
        return self

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

    # 获取前一日的价格数据
    def get_before_data(self, data, i):
        try:
            before_data = data.ix[:i+1, :]
        except:
            before_data = None
        # print('before_data',before_data)
        return before_data

    # 获取信号
    def handle_signal(self, info, data, i):
        today = data.index[i]
        # today_str = datetime.datetime.strftime(today, "%Y-%m-%d %H:%M:%S")
        price = data[data.columns[0]][i]
        try:
            today_next = data.index[i + 1]
        except:
            today_next = np.nan

        try:
            price_next = data[data.columns[0]][i + 1]
        except:
            price_next = np.nan

        self.csv_signal_dict[today] = ''
        self.csv_amount_dict[today] = np.nan
        self.buy_openPrice_dict[today] = np.nan
        self.sell_openPrice_dict[today] = np.nan

        if info:
            if info['type'] == 'limit':
                order_info = {}
                order_info['id'] = info['id']
                order_info['price'] = info['price']
                order_info['symbol'] = info['symbol']
                order_info['date_time'] = today_next
                order_info['side'] = info['side']
                order_info['amount'] = info['amount']
                order_info['type'] = info['type']

                self.historyLimitOrder_list.append(order_info)

            else:
                print('出现信号')
                # print('下一时刻{}-价格{}'.format(today_next, price_next))
                order_info = {}
                order_info['id'] = info['id']
                order_info['price'] = price_next
                order_info['date_time'] = today_next
                order_info['symbol'] = info['symbol']
                order_info['side'] = info['side']
                order_info['amount'] = info['amount']
                order_info['type'] = info['type']

                self.add_info(order_info)

        else:
            print('没有出现信号')
            return {}

    # 添加订单信息
    def add_info(self, order_dict):
        self.historyOrder_list.append(order_dict)

    def handle_balance(self, info_dict):
        first_coin = info_dict['symbol'][0:3]
        end_coin = info_dict['symbol'][-3:]
        symbol_coin = first_coin  + end_coin
        # print(first_coin, end_coin)
        if info_dict['side'] == 'buy':
            # self.balance_dict['BTC'] += float(info_dict['amount'])
            self.balance_dict[first_coin] += float(info_dict['amount']) * float(1 - self.buy_fee)
            self.balance_dict[end_coin] -= float(info_dict['amount']) * float(info_dict['price'])

            self.csv_signal_dict[info_dict['date_time']] = 'buy'
            self.csv_amount_dict[info_dict['date_time']] = float(info_dict['amount'])

            self.buy_openPrice_dict[info_dict['date_time']] = info_dict['price']

        else:
            self.balance_dict[end_coin] += float(info_dict['amount']) * float(info_dict['price'])
            self.balance_dict[first_coin] -= float(info_dict['amount']) * float(1 - self.sell_fee)
            # self.balance_dict['BTC'] -= float(info_dict['amount'])
            self.csv_signal_dict[info_dict['date_time']] = 'sell'
            self.csv_amount_dict[info_dict['date_time']] = float(info_dict['amount'])
            self.sell_openPrice_dict[info_dict['date_time']] = info_dict['price']

        pprint(self.balance_dict)

        # 全部则换成end_coin 值
        info = {}  # 保存现在 和 初始的差值信息
        for sym, val in self.cash.items():
            for new_sym, new_val in self.balance_dict.items():
                # print('cash', self.cash)
                # print('balance', self.balance_dict)
                if sym == new_sym:
                    info[sym] = float(new_val) - float(val)
        print('差值', info)

        self.end_balance = 0
        for _key, _val in info.items():
            if _key == first_coin:
                self.end_balance += float(self.today_symbol_price[symbol_coin]) * float(_val)
            elif _key == end_coin:
                self.end_balance += float(_val)
            else:
                pass
        # print(info_dict)
        # print(end_balance)


    # 转换成一份
    def to_fund(self):
        if self.end_balance == 0:

            self.btc_balance.append(0)
        else:
            self.btc_balance.append(self.end_balance)
        # 按初始金额 以BTC为结算标的
        # info = {}                       # 保存现在 和 初始的差值信息
        # for sym, val in self.cash.items():
        #     for new_sym, new_val in self.balance_dict.items():
        #         print('cash', self.cash)
        #         print('balance', self.balance_dict)
                # if sym == new_sym:
                #     info[sym] = float(new_val) - float(val)
        # print('差值', info)




        # exit()
        # self.today {key :symbol_list}
        # info 各个差值

        # btc_list = []
        # for sy, va in info.items():
        #     if sy != 'BTC':
        #         for symbol, price in self.today_symbol_price.items():
        #             if sy == symbol and sy != 'USD':
        #                 _btc = float(va) * float(price)
        #                 btc_list.append(_btc)
        #             elif sy == symbol and sy == 'USD':
        #                 _btc = float(price) / float(va)
        #                 btc_list.append(_btc)
        #             else:
        #                 pass
        #     else:
        #         btc_list.append(va)
        # btc_balance = sum(btc_list)
        #
        # self.btc_balance.append(self.cash['BTC'] + btc_balance)
        # print('转换成btc', self.btc_balance)

        # exit()

    # 最后一天结算
    def lastday_balance(self):
        # 全部则换成end_coin 值
        info = {}  # 保存现在 和 初始的差值信息
        for sym, val in self.cash.items():
            for new_sym, new_val in self.balance_dict.items():
                # print('cash', self.cash)
                # print('balance', self.balance_dict)
                if sym == new_sym:
                    info[sym] = float(new_val) - float(val)
        print('最后一日差值', info)

        symbol_coin = self.symbol_list[0]
        first_coin = symbol_coin[0:3]
        end_coin = symbol_coin[-3:]
        # print(first_coin, end_coin)
        # exit()
        self.end_balance = 0
        for _key, _val in info.items():
            if _key == first_coin:
                self.end_balance += float(self.today_symbol_price[symbol_coin]) * float(_val)
            elif _key == end_coin:
                self.end_balance += float(_val)
            else:
                pass
        print(self.end_balance)
        self.btc_balance.remove(self.btc_balance[-1])
        self.btc_balance.append(self.end_balance)


        # #########最后一天结算 允许容纳多少量#############
        for _key, _val in self.csv_balance_dict.items():
            symbol_coin = self.symbol_list[0]

            if self.symbol_list[0][0:3] == _key:

                first_abs = max([abs(i) for i in self.csv_balance_dict[_key]])
                self.allow_min_coin_dict[_key] = first_abs
                val1 = first_abs * self.firstday_symbol_price[symbol_coin]
                # print(first_abs)
            elif self.symbol_list[0][-3:] == _key:
                end_abs = max([abs(i) for i in self.csv_balance_dict[_key]])
                self.allow_min_coin_dict[_key] = end_abs
                val2 = end_abs
                # print(end_abs)
            else:
                pass

        # 允许最小的货币量
        min_cash = val1 + val2
        # print(min_cash)
        self.para_allowCash = min_cash

    # 处理数据
    def handle_data(self, data_dict=None, today=None, price_type=None):

        # 获取一组数据 作为遍历的样本 TODO 后期需要更改
        data = data_dict[list(data_dict.keys())[0]]


        self.csv_time_list = data.index
        self.csv_dataPrice_list = data[data.columns[0]].tolist()

        # 生成策略实例对象
        s = Strategy(account=self, strategy_arg=self.strategy_arg)

        for i in range(len(data)):
            if i == 0:
                for _key in data_dict.keys():
                    self.firstday_symbol_price[_key] = data_dict[_key][data_dict[_key].columns[0]][0]

            # 定量 变量值
            today = data.index[i]                    # 时间戳
            print(type(today))
            # exit()
            # today_str = datetime.datetime.strftime(today, "%Y-%m-%d %H:%M:%S")
            price = data[data.columns[0]][i]

            # TODO 获取当天symbol_list 对应的价格 为后续 则和成初始化分数
            for _key in data_dict.keys():
                self.today_symbol_price[_key] = data_dict[_key][data_dict[_key].columns[0]][i]

            # 给实例对象传入当日之前的历史数据
            before_data = self.get_before_data(data, i)

            info_d = {}
            info_d['before_data'] = before_data
            info_d['dataLen'] = i  # 记入数据长度

            # 获取交易信号
            info = s.get_signal(info_d)
            print('当前时刻{}-价格{}'.format(today, price))

            # 处理信号 整合信息
            self.handle_signal(info, data, i)

            # 遍历市价单
            for signal_dict in self.historyOrder_list:
                if today == signal_dict['date_time']:
                    self.handle_balance(signal_dict)

            # 遍历限价单
            for limit_order_index in range(len(self.historyLimitOrder_list)):
                if self.historyLimitOrder_list[limit_order_index]['side'] == 'buy':
                    if price >= self.historyLimitOrder_list[limit_order_index]['price']:
                        print('执行限价单操作--buy')
                        self.handle_balance(self.historyLimitOrder_list[limit_order_index])
                        self.historyLimitOrder_list.remove(self.historyLimitOrder_list[limit_order_index])

                else:
                    if  price <= self.historyLimitOrder_list[limit_order_index]['price']:
                        print('执行限价单操作--sell')
                        self.handle_balance(self.historyLimitOrder_list[limit_order_index])
                        self.historyLimitOrder_list.remove(self.historyLimitOrder_list[limit_order_index])

            # 执行平仓交易
            self.MA = s.MA
            # 添加余额
            for symbol in self.balance_dict.keys():
                l = self.csv_balance_dict[symbol]
                vol = copy.deepcopy(self.balance_dict)

                ll = copy.deepcopy(self.csv_balance_dict[symbol])
                ll.append(vol[symbol])
                self.csv_balance_dict[symbol] = ll

            print(self.csv_balance_dict)
            # TODO 添加相关信息 为可视化输出 服务
            self.to_fund()
        # exit()

        # 最后一个交易日进行结算
        self.lastday_balance()





if __name__ == '__main__':
    pass