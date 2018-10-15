# -*- coding:utf-8 -*-
__author__ = 'xin'

"""
此文件作为历史数据 
"""
import pandas as pd
import os
import datetime
import re

class HistoryData(object):
    def __init__(self):
        pass

    def get_history_data(self, symbol=None, start=None, end=None, type='close', freq=None):
        """
        获取指定的历史数据

        :param symbol:    交易标的
        :param start:     开始时间
        :param end:       结束时间
        :param freq:      数据周期类型
        :return:          返回数据 字典  { symbol : {closePrice:[ , , ,],
                                                     openPrice:[ , , ,],
                                                     highPrice:[ , , ,],
                                                                         }
        """
        # TODO 对应相关时间数据

        data = self.findData(start, end)
        print(data)
        # f = open('E:\\BackTest\\BackTest_v1\\Data\\BITFINEX_BTCUSD_20170101_1T.csv')
        # data = pd.read_csv(f, index_col=0)
        ohlc_dict = {'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'}
        data.index = pd.to_datetime(data.index)
        if freq == '5T':
            return self.get_5T(data, ohlc_dict, type)
        elif freq == '15T':
            return self.get_15T(data, ohlc_dict, type)
        elif freq == '30T':
            return self.get_30T(data, ohlc_dict, type)
        elif freq == '1H':
            return self.get_1H(data, ohlc_dict, type)
        elif freq == '4H':
            return self.get_4H(data, ohlc_dict, type)
        else:
            print('没有对应的时间段数据')

        symbol = 'BTC_USDT'
        history_data = dict()

        ohlc_dict = {'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'}
        data.index = pd.to_datetime(data.index)
        new_data = data.resample('15T', closed='right', label='right').agg(ohlc_dict)


        return new_data

    def get_5T(self, data, ohlc_dict, type):
        new_data = data.resample('5T', closed='right', label='right').agg(ohlc_dict)
        print(new_data)
        if type == 'close':
            # new_data_list = new_data['close'].tolist()
            # print(new_data_list)
            return new_data[['close']]
        elif type == 'open':
            # new_data_list = new_data['open'].tolist()
            # print(new_data_list)
            return new_data[['open']]
        elif type == 'high':
            # new_data_list = new_data['high'].tolist()
            # print(new_data_list)
            return new_data[['high']]
        elif type == 'low':
            # new_data_list = new_data['low'].tolist()
            # print(new_data_list)
            return new_data[['low']]
        else:
            raise TypeError('无 数据')

    def get_15T(self, data, ohlc_dict, type):
        new_data = data.resample('15T', closed='right', label='right').agg(ohlc_dict)
        print(new_data)
        if type == 'close':
            return new_data[['close']]
        elif type == 'open':
            return new_data[['open']]
        elif type == 'high':
            return new_data[['high']]
        elif type == 'low':
            return new_data[['low']]
        else:
            raise TypeError('无 数据')

        pass

    def get_30T(self, data, ohlc_dict, type):
        new_data = data.resample('30T', closed='right', label='right').agg(ohlc_dict)
        print(new_data)
        if type == 'close':
            return new_data[['close']]
        elif type == 'open':
            return new_data[['open']]
        elif type == 'high':
            return new_data[['high']]
        elif type == 'low':
            return new_data[['low']]
        else:
            raise TypeError('无 数据')
        pass

    def get_1H(self, data, ohlc_dict, type):
        new_data = data.resample('1H', closed='right', label='right').agg(ohlc_dict)
        print(new_data)
        if type == 'close':
            return new_data[['close']]
        elif type == 'open':
            return new_data[['open']]
        elif type == 'high':
            return new_data[['high']]
        elif type == 'low':
            return new_data[['low']]
        else:
            raise TypeError('无 数据')

    def get_4H(self, data, ohlc_dict, type):
        new_data = data.resample('4H', closed='right', label='right').agg(ohlc_dict)
        print(new_data)
        if type == 'close':
            return new_data[['close']]
        elif type == 'open':
            return new_data[['open']]
        elif type == 'high':
            return new_data[['high']]
        elif type == 'low':
            return new_data[['low']]
        else:
            raise TypeError('无 数据')
        pass

    # 获取回测日期中的所有日期
    def getEveryDay(self, begin_date, end_date):
        date_list = []
        begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y-%m-%d")
            date_list.append(date_str)
            begin_date += datetime.timedelta(days=1)
        return date_list

    def findData(self, start, end):
        date_list = self.getEveryDay(start, end)
        file_path = 'E:\\BackTest\\BackTest_v1\\Data\\BTCUSD'
        file_list = []
        for i in os.listdir(file_path):
            for j in date_list:
                if re.sub('-', '', j) in i:
                    path = file_path + '\\{}'.format(i)
                    file_list.append(path)
        # print(file_list)
        data = self.appendData(file_list)
        return data

    # TODO 根据不同原始数据文件  需要修改 列名 按照指定的列名写好
    def appendData(self, file_list):
        df_list = []
        for i in file_list:
            df = pd.read_csv(i, header=1,index_col=0)
            df_list.append(df)
        df1 = pd.DataFrame(columns=['candle_begin_time', 'open', 'high', 'low', 'close', 'volume'])
        result = df1.append(df_list)
        # print(result)
        return result


if __name__ == '__main__':
    data = HistoryData().get_history_data(start='2017-01-02', end='2017-01-03', freq='5T',type='open')

    pass












