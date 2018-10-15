# -*- coding:utf-8 -*-
__author__ = 'xin'
"""
此文件总回测文件api  类名称 可以自己命名 方便以后打包成自己的产品
"""
import datetime
from BackTest_v1.Account.accountMain import Account
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from BackTest_v1.Data.dataMain import HistoryData


class OurName(object):
    def __init__(self):
        pass

    def backtest(self, start, end, symbol=None, capital_base=None, price_type='close',freq=None, commission=None,  slippage=None, initialize=None, handle_data=None, refresh_rate=1):
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
        print('ss')
        ################################# 计算开始到结束的交易日日期 ##################################
        date_list = []
        begin_date = datetime.datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end, "%Y-%m-%d")
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y-%m-%d")
            date_list.append(date_str)
            begin_date += datetime.timedelta(days=1)
        ###############################################################################################
        account = Account()
        handle_data = account.handle_data
        account.back_test_date = date_list
        # data = [float(x) for x in range(0, 21)]
        # data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 1.0]
        data = HistoryData().get_history_data(start=start, end=end, type=price_type, freq='5T')
        # print('最终获取的数据', data)
        # print('停止程序')
        # exit()
        for i in range(len(date_list)):
            print('开始回测日期是{}>>>>'.format(date_list[i]))
            # 获取当天之前的数据
            new_data = self.get_before_today_data(start=start, end=date_list[i], data=data)

            # 每日处理数据 传入当天日期
            handle_data(new_data, today=date_list[i], price_type=price_type)

            # 计算每日净值

        print('nameMain--{}'.format(account.allowSell_symbol))
        print(account.__dict__)
        self.report(account)

    # 获取当天之前的交易日日期
    def get_before_today_data(self, start, end, data):
        end_day = datetime.datetime.strptime(end, "%Y-%m-%d")
        print(end_day)
        tomorrow = end_day + datetime.timedelta(days=1)
        print('当天日期获取的数据:', data[data.index <= tomorrow])
        # new_data = data[0:end]
        # print('获取当天日期之前的数据：', new_data)
        return data[data.index <= tomorrow]

    # report 输出报告
    def report(self, account):
        x = account.back_test_date
        y = account.every_balance
        # print(x,y)
        plt.plot(x, y, marker='o')
        # plt.yticks(range(50,150,5))
        plt.xticks(rotation=45)
        plt.ylabel('Balance')
        plt.xlabel('BackTestDate')
        plt.grid(linestyle='-.')
        plt.show()
        # TODO 添加折线图 饼状图等 各图分开写

        pass


if __name__ == '__main__':
    OurName().backtest('2017-07-01', '2017-07-03', price_type='close')




