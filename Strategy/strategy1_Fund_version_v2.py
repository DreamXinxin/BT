# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
__author__ = 'xin'
import talib
import numpy as np
import copy
from Setting.setting import start_date, end_date, init_dict, symbol_history_list, STRATEGY_NAME


class Demo(object):
    def __init__(self):
        self.id_num = 0
        self.limit_order_list = []          # 储存挂单的订单
        pass

    def get_id(self):
        self.id_num += 1
        return self.id_num

    def addOrder(self, info_dict):
        try:
            # 如果是limit单 必须带平仓价
            if info_dict['type'] == 'limit':
                info_dict_cp = copy.deepcopy(info_dict)
                self.limit_order_list.append(info_dict_cp)
            else:
                info_dict_cp = copy.deepcopy(info_dict)
                if info_dict_cp['openPrice'] != np.nan:
                    self.market_open_order_list.append(info_dict_cp)
                elif info_dict_cp['closePrice'] != np.nan:
                    self.market_close_order_list.append(info_dict_cp)
                pass
        except:
            raise TypeError('参数不正确 没有相关的字段')
        pass


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


        self.market_open_order_list = []             # 储存开仓现价的订单
        self.market_close_order_list = []            # 储存开仓现价的订单
        info_dict = {}                               # 返回数据 记录相关信息


        # 使用的技术指标
        MA = talib.MA(np.array(data), timeperiod=10)

        # 开仓信号  满足开仓信号 将flag 赋值为1 返回  需要哪个货币对的数据 就在data_dict中匹配
        if data[dataLen] > MA[dataLen]:                  # 条件语句作为策略开仓信号  自己可更改
            # 如果是其他币种 用第一行代码 表示当前价格
            # Price = data_dict['ETHBTC'][data_dict['ETHBTC'].columns[-1]][dataLen]
            Price = price
            info_dict['id'] = str(self.get_id())
            info_dict['symbol'] = 'BTCUSD'            # 订单交易 货币对
            info_dict['balanceCoin'] = 'USD'         # 结算货币
            info_dict['amount'] = '1'                 # 订单仓位
            info_dict['type'] = 'market'              # 订单类型 limit or market
            info_dict['side'] = 'buy'                 # 订单交易方向 buy orUSD sell
            info_dict['price'] = price                # 当前价格
            info_dict['openPrice'] = Price                # 订单成交价格
            info_dict['datetime'] = date_time         # 订单交易产生的时间
            # 如果订单type为market 则close_price 为 nan
            # 如果订单type为limit  则close_price 需要自己手动填写
            info_dict['closePrice'] = np.nan         # 需要平仓的价格
            info_dict['delLimit'] = '订单id号'        # 需要删除的订单id  如果没有用nan表示
            info_dict['status'] = False

            self.addOrder(info_dict)

            return info_dict

        elif data[dataLen] < MA[dataLen]:
            Price = price
            info_dict['id'] = str(self.get_id())
            info_dict['symbol'] = 'BTCUSD'  # 订单交易 货币对
            info_dict['balanceCoin'] = 'USD'  # 结算货币
            info_dict['amount'] = '1'  # 订单仓位
            info_dict['type'] = 'market'  # 订单类型 limit or market
            info_dict['side'] = 'buy'  # 订单交易方向 buy or sell
            info_dict['price'] = price  # 当前价格
            info_dict['openPrice'] = np.nan  # 订单成交价格
            info_dict['datetime'] = date_time  # 订单交易产生的时间
            # 如果订单type为market 则close_price 为 nan
            # 如果订单type为limit  则close_price 需要自己手动填写
            info_dict['closePrice'] = Price  # 需要平仓的价格
            info_dict['delLimit'] = '填写要扯单订单id号'  # 需要删除的订单id  如果没有用nan表示
            info_dict['status'] = False

            self.addOrder(info_dict)

            return info_dict

        else:
            info_dict['id'] = np.nan
            info_dict['symbol'] = np.nan  # 订单交易 货币对
            info_dict['balanceCoin'] = np.nan  # 结算货币
            info_dict['amount'] = np.nan  # 订单仓位
            info_dict['type'] = np.nan  # 订单类型 limit or market
            info_dict['side'] = np.nan  # 订单交易方向 buy or sell
            info_dict['price'] = price         # 当前价格
            info_dict['openPrice'] = np.nan    # 订单成交价格
            info_dict['datetime'] = date_time  # 订单交易产生的时间
            # 如果订单type为market 则close_price 为 nan
            # 如果订单type为limit  则close_price 需要自己手动填写
            info_dict['closePrice'] = np.nan  # 需要平仓的价格
            info_dict['delLimit'] = np.nan  # 需要删除的订单id  如果没有用nan表示
            info_dict['status'] = False

            return info_dict



if __name__ == '__main__':
     Demo()
