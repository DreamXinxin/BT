# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
__author__ = 'xin'

"""
此文件是创建虚拟账户 
"""
from Data.dataMain import HistoryData
from pprint import pprint
import talib
import numpy as np
from collections import OrderedDict
import datetime
from Strategy.strategyFutureMain import Strategy


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
        self.cash = init_dict['cash']['BTC']                            # 初始金额
        self.balance_dict = init_dict['cash']['BTC']                   # 账户余额
        self.free_cash = init_dict['cash']['BTC']                     # 可使用资金
        self.free_cash_list = []
        self.used_cash = 0                       # 已用资金  使用的保证金
        self.used_cash_list = []
        self.openOrder_list = []                    # 记录开仓订单
        self.closeOrder_list = []                    # 记录平仓订单
        self.openDate_list = []
        self.closeDate_list = []
        self.allowCloseOrder_list = []               # 可卖标的
        self.trade_date = []                         # 交易日日期
        self.back_test_date = []                     # 回测日期
        self.every_balance = []                      # 每日净值
        self.historyOrder_list = []                  # 历史订单

        self.Order = Order                           # 下单模块

        self.open_fee = init_dict['fee']['open_fee']                          # 开仓手续费
        self.close_fee = init_dict['fee']['close_fee']                         # 平仓手续费

        self.csv_time_list = []
        self.csv_balance_list = []
        self.csv_openPrice_dict = {}
        self.csv_closePrice_dict = {}
        self.csv_dataPrice_list = []

        self.zhibiao = None

    # 获取历史订单
    def get_user_history_orders(self):
        # print('获取历史订单', self.historyOrder_list)
        return self.historyOrder_list

    # 获取持仓单
    def get_user_orders(self):
        return self.allowCloseOrder_list

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
        self.csv_openPrice_dict[today] = ''
        self.csv_closePrice_dict[today] = ''
        if info:
            if info['type'] == 'limit':

                raise TypeError('目前不支持limit单')

            else:
                print('出现信号{}-类型{}-状态{}'.format(today, info['side'], info['status']))
                # TODO 发现交易信号时 用下一时刻的信息进行交易
                print('下一时刻{}-价格{}'.format(today_next, price_next))
                order_info = {}
                order_info['price'] = price_next
                order_info['date_time'] = today_next
                order_info['status'] = info['status']
                order_info['side'] = info['side']
                order_info['amount'] = info['amount']
                order_info['type'] = info['type']

                self.add_info(order_info)

        else:
            print('没有出现信号')
            return {}

    # 添加订单信息
    def add_info(self, order_dict):

        if order_dict['status'] == 'open':
            self.openOrder_list.append(order_dict)
            self.openDate_list.append(order_dict['date_time'])
            self.closeDate_list.append('')
            self.allowCloseOrder_list.append(order_dict)

        else:
            self.closeOrder_list.append(order_dict)
            self.closeDate_list.append(order_dict['date_time'])
            self.openDate_list.append('')

    # 添加历史订单信息
    def add_history_orders(self, open_dict, close_dict):
        history_order_dict = {}
        history_order_dict['type'] = open_dict['type']
        history_order_dict['side'] = open_dict['side']
        history_order_dict['amount'] = open_dict['amount']
        history_order_dict['openPrice'] = open_dict['price']
        history_order_dict['closePrice'] = close_dict['price']
        history_order_dict['openDate'] = open_dict['date_time']
        history_order_dict['closeDate'] = close_dict['date_time']
        if open_dict['side'] == 'buy':
            history_order_dict['profit'] = (close_dict['price'] - open_dict['price']) * float(open_dict['amount'])
        else:
            history_order_dict['profit'] = (open_dict['price'] - close_dict['price']) * float(open_dict['amount'])
        # TODO 如果订单添加新的字段 该函数也需要添加对应的字段

        self.historyOrder_list.append(history_order_dict)
        # pprint(self.historyOrder_list)
        pass

    # 处理净值
    def handle_balance(self, info_dict, today, price):
        print(info_dict)
        if info_dict['status'] == 'open':
            print('#####---开仓了---#####')
            fee = float(info_dict['amount']) * float((info_dict['price'])) * self.open_fee * (-1)
            print('#####--扣手续费-{}--####'.format(fee))
            self.balance_dict += fee
            print('####--当前余额-{}-'.format(self.balance_dict))
        else:
            print('+++++ -- 平仓了---+++++')
            if info_dict['side'] == 'sell':
                print('做空单')
                profit = float(info_dict['amount']) * float((price - info_dict['price']))
                print('利润{}---开仓价格-{}--平仓价格-{}'.format(profit, price, info_dict['price']))
                fee = float(info_dict['amount']) * float((info_dict['price'])) * self.open_fee * (-1)
                print('手续费{}'.format(fee))
                self.balance_dict = self.balance_dict + profit + fee
                print('+++++---当前余额--{}--++++'.format(self.balance_dict))
            else:
                print('做多单')

                profit = float(info_dict['amount']) * float((info_dict['price'] - price))
                print('利润{}--开仓价格-{}--平仓价格-{}'.format(profit, price, info_dict['price']))
                fee = float(info_dict['amount']) * float((info_dict['price'])) * self.open_fee * (-1)
                print('手续费{}'.format(fee))
                self.balance_dict = self.balance_dict + profit + fee
                print('+++++---当前余额--{}--++++'.format(self.balance_dict))

    # 处理数据
    def handle_data(self, data_dict=None, today=None, price_type=None):

        # 获取一组数据 作为遍历的样本 TODO 后期需要更改
        data = data_dict[list(data_dict.keys())[0]]
        self.csv_time_list = data.index
        self.csv_dataPrice_list = data[data.columns[0]].tolist()

        # 生成策略实例对象
        s = Strategy(account=self, strategy_arg=self.strategy_arg)

        for i in range(len(data)):
            # 定量 变量值
            today = data.index[i]                    # 时间戳
            # today_str = datetime.datetime.strftime(today, "%Y-%m-%d %H:%M:%S")
            price = data[data.columns[0]][i]

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

            # 执行下单交易

            for openOrder_dict in self.openOrder_list:
                if today == openOrder_dict['date_time']:
                    print('执行下单交易-日期{}-价格{}'.format(today, openOrder_dict['price']))
                    # TODO 下单函数
                    self.csv_openPrice_dict[today] = openOrder_dict['price']

                    # TODO 净值计算 对应时间 如果有开仓信号 按下一日的时间计算
                    self.handle_balance(openOrder_dict, today, price)


            # 执行平仓交易
            if self.closeOrder_list:
                for closeSignal_dict in self.closeOrder_list:
                    if today == closeSignal_dict['date_time'] and len(self.allowCloseOrder_list) > 0:
                        # TODO 后续版本需要改 对于一个时间段平多数量订单
                        for allowCloseOrder in self.allowCloseOrder_list:
                            print(allowCloseOrder)
                            open_price = allowCloseOrder['price']
                            print('执行平仓交易-日期{}-价格{}'.format(today, closeSignal_dict['price']))
                            # TODO 平仓操作
                            self.csv_closePrice_dict[today] = closeSignal_dict['price']
                            # TODO 净值计算 对应时间 如果有开仓信号 按下一日的时间计算
                            self.handle_balance(closeSignal_dict, today, open_price)
                            # 添加到历史订单
                            self.add_history_orders(open_dict=allowCloseOrder, close_dict=closeSignal_dict)
                            # 将改订单删除
                            self.allowCloseOrder_list.remove(allowCloseOrder)



            self.MA = s.MA
            # 添加余额
            self.csv_balance_list.append(self.balance_dict)


            # TODO 添加相关信息 为可视化输出 服务

            pass
        # exit()


if __name__ == '__main__':
    pass