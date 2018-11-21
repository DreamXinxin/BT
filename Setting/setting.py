# -*- coding:utf-8 -*-
"""
初始化参数文件
"""

# 回测日期
start_date = '2017-07-01'
end_date = '2017-07-01'

# 技术指标初始值
START = 5
END = 15
# 技术指标步长
STEP = 5

# 初始账户金额
init_dict = {
        'BTC': 1000.0,
        'USD': 10000.0,
        'ETH': 5000.0,
    }

# 需要获取的多币种的历史数据
symbol_history_list = ['BTCUSD', ]

# 需要使用的策略 填写策略文件名
STRATEGY_NAME = 'strategy1'




# import sys
# c = '/Users/billy/PycharmProjects/BackTest/BackTest_v1/Name'
# sys.path.append(c)
# f = __import__('nameMain')
# f.OurName().backtest('2017-07-01', '2017-07-02', price_type='close')












