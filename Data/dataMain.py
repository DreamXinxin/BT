# -*- coding:utf-8 -*-
__author__ = 'xin'

"""
此文件作为历史数据 
"""
import pandas as pd
import os
import datetime
import re
import pymongo
import time
import pytz
from dateutil import parser
import numpy as np


class HistoryCSVData(object):
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

        data = self.findData(start, end, symbol)
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



        # ohlc_dict = {'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'}
        # data.index = pd.to_datetime(data.index)
        # new_data = data.resample(freq, closed='right', label='right').agg(ohlc_dict)

        # return new_data

    def get_5T(self, data, ohlc_dict, type):
        new_data = data.resample('5T', closed='right', label='right').agg(ohlc_dict)
        print(new_data)
        if type == 'close':
            # new_data_list = new_data['close'].tolist()
            # print(new_data_list)
            return new_data[['close', 'volume']]
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

    def findData(self, start, end, symbol):
        date_list = self.getEveryDay(start, end)
        file_path = '/Users/billy/PycharmProjects/BackTest/BackTest_v1/Data/{}'.format(symbol)
        file_list = []
        for i in os.listdir(file_path):
            for j in date_list:
                if re.sub('-', '', j) in i:
                    path = file_path + '/{}'.format(i)
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


class HistoryDBData(object):
    def __init__(self):

        # 远程连接部分
        user = 'root'
        pwd = 'Shixin2018$'
        host = '47.75.243.109'
        port = '27017'
        db_name ='kline__'
        # uri = "mongodb://%s:%s@%s" % (user, pwd, host + ":" + port + "/" + db_name)
        # self.client = pymongo.MongoClient(uri)
        # self.db = self.client['BN_BTC_USDT_1h']
        host = '47.75.243.109'
        self.client = pymongo.MongoClient(host)
        # self.client.adb.authenticate(user, pwd, mechanism='SCRAM-SHA-1')
        self.db = self.client[db_name]

        # 本地连接
        # self.client = pymongo.MongoClient(host='localhost', port=27017)
        # self.db = self.client['kline']['BN_BTC_USDT_1h']

    def closeDB(self):
        self.client.close()

    def get_start_end(self, start, end):
        start_str = datetime.datetime.strptime(start, '%Y-%m-%d')
        start = start_str - datetime.timedelta(hours=8)
        start = datetime.datetime.strftime(start, '%Y-%m-%d %H:%M:%S')
        end_str = datetime.datetime.strptime(end, '%Y-%m-%d')
        end = end_str - datetime.timedelta(hours=8)
        end = datetime.datetime.strftime(end, '%Y-%m-%d %H:%M:%S')
        start = re.sub(' ', '{}', start)
        start = start.format('T') + 'Z'
        end = re.sub(' ', '{}', end)
        end = end.format('T') + 'Z'
        return start, end

    def get_history_data(self, symbol='BTCUSDT', start=None, end=None, type='close', freq=None):
        # 先将日期减去8小时
        start, end = self.get_start_end(start, end)

        queryArgs = {"$and":[{"Time":{"$gt":start}},{"Time":{"$lt":end}}]}

        if symbol in ['BTCUSD','EOSBTC', 'EOSETH', 'EOSUSD','ETCBTC', 'ETCUSD', 'ETHBTC', 'ETHUSD',
                        'LTCBTC','LTCUSD']:
            db = self.db['BF_' + symbol[:3] + '_' + symbol[-3:] + '.BF_1m']
        else:
            err = '目前该交易所没有该{}货币对数据'.format(symbol)
            raise TypeError(err)

        data = db.find(queryArgs)

        df = pd.DataFrame(list(data))
        try:
            df = df.drop_duplicates(['Time'])
        except:
            raise TypeError('目前没有该时间段的数据')

        del df['_id']
        for utc_str in df['Time']:
            local_time = self.utc_to_local(utc_str)
            df['Time'].replace(utc_str, local_time, inplace=True)

        data = df[['Open', 'Close', 'High', 'Low', 'QuoteAssetVolume', 'QuoteVolume', 'Time']].set_index('Time')
        data.rename(columns={'Open': 'open', 'Close': 'close', 'High': 'high', 'Low':'low'}, inplace=True)
        ohlc_dict = {'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'QuoteVolume': 'sum', 'QuoteAssetVolume':'sum'}
        data[['open', 'close', 'high', 'low','QuoteAssetVolume', 'QuoteVolume']] = data[['open', 'close', 'high', 'low','QuoteAssetVolume', 'QuoteVolume']].astype(float)
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

    def get_5T(self, data, ohlc_dict, type):
        new_data = data.resample('5T', closed='right', label='right').agg(ohlc_dict)
        print(new_data)
        if type == 'close':
            return new_data[['close', 'QuoteAssetVolume', 'QuoteVolume']]
        elif type == 'open':
            return new_data[['open', 'QuoteAssetVolume', 'QuoteVolume']]
        elif type == 'high':
            return new_data[['high', 'QuoteAssetVolume', 'QuoteVolume']]
        elif type == 'low':
            return new_data[['low', 'QuoteAssetVolume', 'QuoteVolume']]
        else:
            raise TypeError('无 数据')

    def get_15T(self, data, ohlc_dict, type):
        new_data = data.resample('15T', closed='right', label='right').agg(ohlc_dict)
        print(new_data)
        if type == 'close':
            return new_data[['close', 'QuoteAssetVolume', 'QuoteVolume']]
        elif type == 'open':
            return new_data[['open', 'QuoteAssetVolume', 'QuoteVolume']]
        elif type == 'high':
            return new_data[['high', 'QuoteAssetVolume', 'QuoteVolume']]
        elif type == 'low':
            return new_data[['low', 'QuoteAssetVolume', 'QuoteVolume']]
        else:
            raise TypeError('无 数据')

    def get_30T(self, data, ohlc_dict, type):
        new_data = data.resample('30T', closed='right', label='right').agg(ohlc_dict)
        print(new_data)
        if type == 'close':
            return new_data[['close', 'QuoteAssetVolume', 'QuoteVolume']]
        elif type == 'open':
            return new_data[['open', 'QuoteAssetVolume', 'QuoteVolume']]
        elif type == 'high':
            return new_data[['high', 'QuoteAssetVolume', 'QuoteVolume']]
        elif type == 'low':
            return new_data[['low', 'QuoteAssetVolume', 'QuoteVolume']]
        else:
            raise TypeError('无 数据')

    def get_1H(self, data, ohlc_dict, type):
        new_data = data.resample('1H', closed='right', label='right').agg(ohlc_dict)
        print(new_data)
        if type == 'close':
            return new_data[['close', 'QuoteAssetVolume', 'QuoteVolume']]
        elif type == 'open':
            return new_data[['open', 'QuoteAssetVolume', 'QuoteVolume']]
        elif type == 'high':
            return new_data[['high', 'QuoteAssetVolume', 'QuoteVolume']]
        elif type == 'low':
            return new_data[['low', 'QuoteAssetVolume', 'QuoteVolume']]
        else:
            raise TypeError('无 数据')

    def get_4H(self, data, ohlc_dict, type):
        new_data = data.resample('4H', closed='right', label='right').agg(ohlc_dict)
        print(new_data)
        if type == 'close':
            return new_data[['close', 'QuoteAssetVolume', 'QuoteVolume']]
        elif type == 'open':
            return new_data[['open', 'QuoteAssetVolume', 'QuoteVolume']]
        elif type == 'high':
            return new_data[['high', 'QuoteAssetVolume', 'QuoteVolume']]
        elif type == 'low':
            return new_data[['low', 'QuoteAssetVolume', 'QuoteVolume']]
        else:
            raise TypeError('无 数据')

    def utc_to_local(self, utc_time_str, utc_format='%Y-%m-%d %H:%M:%S'):
        utc_datetime = parser.parse(utc_time_str)
        utc_datetime += datetime.timedelta(hours=8)
        local_time = utc_datetime.strftime(utc_format)
        return local_time


if __name__ == '__main__':
    # data = HistoryCSVData().get_history_data(start='2017-01-02', end='2017-01-03', freq='5T',type='open')
    mongo = HistoryDBData()
    data_df = mongo.get_history_data(symbol='BTCUSD', start='2017-07-16', end='2017-07-18', type='close', freq='4H')
    print(data_df)
    mongo.closeDB()











