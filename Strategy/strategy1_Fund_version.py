# -*- coding:utf-8 -*-
__author__ = 'xin'
import talib
import numpy as np
from Setting.setting import start_date, end_date, init_dict, symbol_history_list, STRATEGY_NAME


class Demo(object):
    def __init__(self):
        self.id_num = 0
        self.limit_order_list = []          # 储存挂单的订单

        pass

    def get_id(self):
        self.id_num += 1
        return self.id_num

    def run(self, info_d):
        price = info_d['price']          # 当时时间点对应的价格
        date_time = info_d['datetime']   # 时间点
        dataLen = info_d['dataLen']      # 总数据中遍历到 哪部分的长度
        data_dict = info_d['data_dict']            # 回测周期  各个币种的全部数据
        # print('data_dict:', data_dict)
        # exit()

        # for symbol,symbol_data in data_dict.items():
        #     print(symbol)

        # ############################### 编写自己的交易策略 ##########################################
        # data = data_dict[list(data_dict.keys())[0]]
        try:
            data = data_dict[list(data_dict.keys())[0]]['close']
        except:
            try:
                data = data_dict[list(data_dict.keys())[0]]['open']
            except:
                try:
                    data = data_dict[list(data_dict.keys())[0]]['high']
                except:
                    data = data_dict[list(data_dict.keys())[0]]['low']

        # 使用的技术指标
        MA = talib.MA(np.array(data), timeperiod=10)

        # 开仓信号  满足开仓信号 将flag 赋值为1 返回  需要哪个货币对的数据 就在data_dict中匹配
        if data[dataLen] > MA[dataLen]:                  # 条件语句作为策略开仓信号  自己可更改

            # TODO 返回的数据 字典  price vol datetime
            # TODO 挂单需要返回 多加条 需要平仓价格
            open_list = []                               # 将所有需要交易的订单 保存到list
            #
            ############# 一组数据 ################
            # open_info_dict = {}
            # Price = price
            # open_info_dict['id'] = str(self.get_id())
            # open_info_dict['symbol'] = 'BTCUSD'          # 订单交易 货币对
            # open_info_dict['balance_coin'] = 'USD'       # 结算货币
            # open_info_dict['amount'] = '1'               # 订单仓位
            # open_info_dict['type'] = 'market'            # 订单类型 limit or market
            # open_info_dict['side'] = 'buy'               # 订单交易方向 buy or sell
            # open_info_dict['price'] = Price              # 订单成交价格
            # open_info_dict['datetime'] = date_time       # 订单交易产生的时间
            # 下一版本应用
            # open_info_dict['status'] = 'open'            # 订单状态需要开仓的 open or close

            # open_list.append(open_info_dict)
            #
            # # ############  二组数据 ###############
            open_info_dict = {}
            Price = data_dict['ETHBTC'][data_dict['ETHBTC'].columns[-1]][dataLen]
            open_info_dict['id'] = str(self.get_id())
            open_info_dict['symbol'] = 'ETHBTC'            # 订单交易 货币对
            open_info_dict['balance_coin'] = 'BTC'         # 结算货币
            open_info_dict['amount'] = '1'                 # 订单仓位
            open_info_dict['type'] = 'market'              # 订单类型 limit or market
            open_info_dict['side'] = 'buy'                 # 订单交易方向 buy or sell
            open_info_dict['price'] = Price                # 订单成交价格
            open_info_dict['datetime'] = date_time         # 订单交易产生的时间
            # 如果订单type为market 则close_price 为 nan
            # 如果订单type为limit  则close_price 需要自己手动填写
            open_info_dict['close_price'] = np.nan()       # 需要平仓的价格


            open_list.append(open_info_dict)

            flag = 1
            return flag, open_list
        # 平仓信号
        elif data[dataLen] < MA[dataLen]:                # # 条件语句作为策略开仓信号  自己可更改
            close_list = []  # 将所有需要交易的订单 保存到list

            # ############# 一组数据 ################
            # close_info_dict = {}
            # Price = price
            # close_info_dict['id'] = '1'                 # 如果选择平仓 指定id号码
            # close_info_dict['symbol'] = 'BTCUSD'        # 订单交易 货币对
            # close_info_dict['balance_coin'] = 'USD'     # 结算货币
            # close_info_dict['amount'] = '1'             # 订单仓位
            # close_info_dict['type'] = 'market'          # 订单类型 limit or market
            # close_info_dict['side'] = 'buy'             # 订单交易方向 buy or sell
            # close_info_dict['price'] = Price            # 订单成交价格
            # close_info_dict['datetime'] = date_time     # 订单交易产生的时间
            # 下一版本应用
            # close_info_dict['status'] = 'open'            # 订单状态需要开仓的 open or close

            # close_list.append(close_info_dict)

            # # ############  二组数据 ###############
            close_info_dict = {}
            Price = data_dict['ETHBTC'][data_dict['ETHBTC'].columns[-1]][dataLen]
            close_info_dict['id'] = '2'                 # 如果选择平仓 指定id号码
            close_info_dict['symbol'] = 'ETHBTC'        # 订单交易 货币对
            close_info_dict['balance_coin'] = 'BTC'     # 结算货币
            close_info_dict['amount'] = '1'             # 订单仓位
            close_info_dict['type'] = 'market'          # 订单类型 limit or market
            close_info_dict['side'] = 'buy'             # 订单交易方向 buy or sell
            close_info_dict['price'] = Price            # 订单成交价格
            close_info_dict['datetime'] = date_time     # 订单交易产生的时间
            close_info_dict['close_price'] = np.nan()

            close_list.append(close_info_dict)
            flag = -1
            return flag, close_list
        else:
            _list = []
            flag = 0
            return flag, _list


if __name__ == '__main__':
     Demo()
