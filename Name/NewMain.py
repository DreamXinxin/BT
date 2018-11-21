# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
__author__ = 'xin'
"""
此文件总回测文件api  类名称 可以自己命名 方便以后打包成自己的产品
"""
import datetime
from Account.accountNew import Account
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from Data.dataMain import HistoryData
import os
from pprint import pprint
import threading
import time



class OurName(object):
    def __init__(self):
        pass

    def backtest(self, start, end, init_dict=None, arg=None,capital_base=None, price_type='close',freq=None, commission=None,  slippage=None, initialize=None, handle_data=None, refresh_rate=1):
        """
        主要回测函数

        :param start:                         起始交易日
        :param end:                           终止交易日
        :param symbol:                        交易标的
        :param capital_base:                  起始资金
        :param freq:                          回测频率
        :param initialize:                    交易策略 -- 虚拟账户初始函数
        :param handle_data:                   交易策略 -- 每日交易指令 判断函数
        :param commission:                    手续费（买/卖）
        :param slippage:                      滑点标准
        :param refresh_rate:                  调仓间隔
        :return:                              回测报告（pandas.DataFrame） 回测数据（Account）
        """
        self.symbol_list = init_dict['symbol_list']
        ################################# 计算开始到结束的交易日日期 ##################################
        date_list = []
        begin_date = datetime.datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end, "%Y-%m-%d")
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y-%m-%d")
            date_list.append(date_str)
            begin_date += datetime.timedelta(days=1)
        ###############################################################################################
        account = Account(init_dict, arg)
        handle_data = account.handle_data
        account.back_test_date = date_list


        data_dict = {}
        for symbol in self.symbol_list:
            data_dict[symbol] = HistoryData().get_history_data(symbol=symbol, start=start, end=end, type=price_type,
                                                               freq=freq)
        print('最终获取的数据', data_dict)

        self.data_dict = data_dict
        # 每日处理数据 传入当天日期
        handle_data(data_dict,  price_type=price_type)

        # 计算每日净值
        print(account.__dict__)
        sharpe_ratio = self.create_sharpe_ratio(account)
        drawmax_draw_down = self.create_drawdowns(account)

        self.outputData(account, start, end)
        self.report(account)

        return ('夏普指数:{}'.format(sharpe_ratio), '最大回撤:{}'.format(drawmax_draw_down))

    # 获取当天之前的交易日日期
    def get_before_today_data(self, start, end, data):
        end_day = datetime.datetime.strptime(end, "%Y-%m-%d")
        print(end_day)
        tomorrow = end_day + datetime.timedelta(days=1)
        print('当天日期获取的数据:', data[data.index <= tomorrow])
        # new_data = data[0:end]
        # print('获取当天日期之前的数据：', new_data)
        return data[data.index <= tomorrow]

    # 输出csv文件
    def outputData(self, account, star, end):
        # print('time', len(account.csv_time_list))
        # print('data', len(account.csv_dataPrice_list))
        # print('open', len(account.csv_openPrice_dict))
        # print('close', len(account.csv_closePrice_dict))

        df = pd.DataFrame()
        df['time'] = account.csv_time_list
        df['time_balance'] = account.csv_balance_list
        df['open_price'] = [account.csv_openPrice_dict[i] for i in sorted(account.csv_openPrice_dict.keys())]
        df['close_price'] = [account.csv_closePrice_dict[i] for i in sorted(account.csv_closePrice_dict.keys())]
        df['data_price'] = account.csv_dataPrice_list
        df['MA'] = account.MA
        file_name = star + '_' + end

        n = 1
        while 1:
            csv_path = '../outputData/{}_balance_{}.csv'
            isExists = os.path.exists(csv_path.format(file_name, n))
            print(n)
            csv_path = csv_path.format(file_name, n)
            if isExists:
                csv_path = csv_path.format(file_name, n)
                print(csv_path)
                n += 1
            else:
                break
        df.to_csv(csv_path, index=False)
        pass

    # report 输出报告
    def report(self, account):
        fig = plt.figure(1)  # 创建第一个画板（figure）
        plt.subplot(211)  # 第一个画板的第一个子图

        # 指定X轴的以日期格式（带小时）显示
        # ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d  %H:%M:%S'))

        y = account.csv_balance_list
        x = account.csv_time_list
        x = [datetime.datetime.strftime(s, "%Y-%m-%d %H:%M:%S") for s in x]
        _y = account.csv_dataPrice_list
        #
        # plt.tight_layout(pad=0.4, w_pad=3.0, h_pad=3.0)
        plt.plot(np.array(x), np.array(y), label='balance')
        plt.xticks(np.array(x)[::10], np.array(x)[0::10], rotation=45)
        plt.ylabel('Balance')
        plt.xlabel('BackTestDate')
        # # plt.yticks(np.array(y)[::10], np.array(y)[::10])
        plt.subplot(212)  # 第二个画板的第二个子图
        # plt.figure(2)  # 创建第一个画板（figure）

        plt.plot(np.array(x), np.array(_y), label='dataPrice')
        plt.plot(np.array(x), np.array(account.MA))
        plt.xticks(np.array(x)[::3], np.array(x)[::3], rotation=45)
        plt.ylabel('DataPrice')
        plt.xlabel('BackTestDate')

        # plt.grid(linestyle='-.')
        # plt.legend()
        # plt.show()
        # plt.pause(2)

        plt.show()
        # TODO 添加折线图 饼状图等 各图分开写

        pass

    # 输出策略评价
    def create_sharpe_ratio(self, account):
        returns = pd.Series(account.csv_balance_list).pct_change()

        sharpe_ratio = np.sqrt(1) * np.mean(returns)/np.std(returns)
        print('夏普系数:', sharpe_ratio)
        return sharpe_ratio

    # 最大回撤
    def create_drawdowns(self, account):
        returns = account.csv_balance_list
        max_draw_down = 0
        temp_max_value = 0
        for i in range(1, len(returns)):
            temp_max_value = max(temp_max_value, returns[i - 1])
            max_draw_down = min(max_draw_down, returns[i] / temp_max_value - 1)
        print('最大回撤系数:', max_draw_down)
        return max_draw_down

if __name__ == '__main__':
    # 回测日期
    start_date = '2017-07-01'
    end_date = '2017-07-01'
    # 需要的货币历史数据
    symbol_list = ['BTCUSD', 'ETHBTC']
    # 账户初始化 相关信息 金额
    init_dict = {
        'cash':{
            'BTC': 10000.0,
            'USD': 10000.0,
            # 'ETH': 5000.0,
        },
        'fee':{
            'open_fee': 0.001,              # 开仓手续费
            'close_fee': 0.001,             # 平仓手续费
        },
        'symbol_list': symbol_list

    }
    # 技术指标初始值
    START = 5
    END = 15
    # 技术指标步长
    STEP = 10

    # 回测周期
    freq = '30T'

    info = {}
    for i in range( START, END, STEP):
        r = OurName()
        info[i] = r.backtest(start=start_date,
                             end=end_date,
                             price_type='close',
                             init_dict=init_dict,
                             freq=freq,
                             arg=i)
        pprint(info)



