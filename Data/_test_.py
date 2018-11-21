# -*- coding:utf-8 -*-
__author__ = 'xin'
"""
测试文件
"""

import pandas as pd
import os
import shutil
import re
import datetime
import zipfile
import matplotlib.pyplot as plt

# file = 'BITFINEX_BTCUSD_2017-07-01_2017-09-30_1H.csv'
# data = pd.read_csv(file)
# print(data.head(5))
# # 获取当前文件夹的 绝对路径
# cur_path = os.path.abspath(os.curdir)
# print(cur_path)

# # 创建文件夹
# goal_path = cur_path + '\\'+'sss'
# os.mkdir(goal_path)

# # os.listdir 查看当前文件夹下的 文件和 文件夹
data_path = 'E:\\BackTest\\BackTest_v1\\Data\\historyData'
# dirs = os.listdir(data_path)
# for di in dirs:
#     print(di)

info = os.walk(data_path)

####################### 数据移动  #####################
old_data = 'E:\\BackTest\\BackTest_v1\\Data\\historyData\\'
# new_data = 'E:\\BackTest\\BackTest_v1\\Data\\BTCUSD\\BITFINEX_BTCUSD_20170101_1H.csv'
# shutil.copy(old_data, new_data)
#
#
# dirs = os.listdir(old_data)
# for i in dirs:
#     file_path = os.path.join(old_data, i)
#     print(file_path)
#     for k in os.listdir(file_path):
#         new_path = os.path.join(file_path, k)
#         print(new_path)
#         if 'BTCUSD' in str(new_path):
#             for j in os.listdir(new_path):
#                 path = os.path.join(new_path, j)
#                 if '1T' in str(path):
#                     print(j)
                    # print(path)
                    # shutil.copy(path, 'E:\\BackTest\\BackTest_v1\\Data\\BTCUSD\\{}'.format(j))
                # print(path)
#
#
# for dirpath, dirnames, filenames in os.walk(old_data):
#     for filepath in filenames:
#         if 'ETHUSD' in str(filepath) and '1T' in str(filepath):
#             path = os.path.join(dirpath, filepath)
#             fileName = re.findall(r'ETHUSD\\(.*)?', path)[0]
#             fileName = path.split('\\')[-1]
            # isExists = os.path.exists('E:\\BackTest\\BackTest_v1\\Data\\ETHUSD\\{}'.format(fileName))
            # if not isExists:
            #     shutil.copy(path, 'E:\\BackTest\\BackTest_v1\\Data\\ETHUSD\\{}'.format(fileName))
            #     print(fileName)
            # else:
            #     print('存在该文件')
#

#####################  数据整合 ###############################
# startTime = '2017-01-02'
# endTime = '2017-01-03'
#
# def getEveryDay(begin_date,end_date):
#     date_list = []
#     begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
#     end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d")
#     while begin_date <= end_date:
#         date_str = begin_date.strftime("%Y-%m-%d")
#         date_list.append(date_str)
#         begin_date += datetime.timedelta(days=1)
#     return date_list
#
# date_list = getEveryDay(startTime, endTime)
# print(date_list)
#
# file_path = 'E:\\BackTest\\BackTest_v1\\Data\\BTCUSD'
# file_list = []
# for i in os.listdir(file_path):
#     for j in date_list:
#         if re.sub('-', '', j) in i:
#             path = file_path + '\\{}'.format(i)
#             file_list.append(path)
# print(file_list)
#
# df_list = []
# for i in file_list:
#     df = pd.read_csv(i, header=1)
#     df_list.append(df)
#     print(df)


# df1 = pd.DataFrame(columns=['candle_begin_time', 'open', 'high', 'low', 'close', 'volume'])
# result = df1.append(df_list)
# print(result)


##############   解压文件 ###################
# file_path = 'E:\\BaiduNetdiskDownload\\_files\\'
# for dirpath in os.listdir(file_path):
#     if '.zip' in dirpath:
#         path = os.path.join(file_path, dirpath)
#         print(path)
        # zip_file = zipfile.ZipFile(path)
        # print(zipfile)
        # for names in zip_file.namelist():
        #     zip_file.extract(names, file_path + dirpath.split('.zip')[0])

############  移动 创建文件 ##############
symbol_list = ['ABSUSD', 'AGIBTC', 'AGIETH', 'AGIUSD', 'AIDBTC', 'AIDETH', 'AIDUSD', 'AIOBTC', 'AIOETH', 'AIOUSD', 'ANTBTC', 'ANTUSD', 'ATMBTC', 'ATMETH', 'ATMUSD', 'AUCBTC', 'AUCETH', 'AUCUSD', 'AVTBTC', 'AVTETH', 'AVTUSD', 'BATBTC', 'BATETH', 'BATUSD', 'BBNUSD', 'BCHBTC', 'BCHETH', 'BCHUSD', 'BCIBTC', 'BCIUSD', 'BFTBTC', 'BFTETH', 'BFTUSD', 'BNTUSD', 'BTCEUR', 'BTCGBP', 'BTCJPY', 'BTCUSD', 'BTGBTC', 'BTGUSD', 'CBTBTC', 'CBTETH', 'CBTUSD', 'CFIBTC', 'CFIUSD', 'CNDBTC', 'CNDETH', 'CNDUSD', 'CTXBTC', 'CTXETH', 'CTXUSD', 'DADBTC', 'DADETH', 'DADUSD', 'DAIBTC', 'DAIETH', 'DAIUSD', 'DATBTC', 'DATETH', 'DATUSD', 'DGXETH', 'DGXUSD', 'DSHBTC', 'DSHUSD', 'DTABTC', 'DTAUSD', 'DTHBTC', 'DTHETH', 'DTHUSD', 'EDOBTC', 'EDOETH', 'EDOUSD', 'ELFBTC', 'ELFETH', 'ELFUSD', 'EOSBTC', 'EOSETH', 'EOSEUR', 'EOSGBP', 'EOSJPY', 'EOSUSD', 'ESSBTC', 'ESSETH', 'ESSUSD', 'ETCBTC', 'ETCUSD', 'ETHBTC', 'ETHEUR', 'ETHGBP', 'ETHJPY', 'ETHUSD', 'ETPBTC', 'ETPETH', 'ETPUSD', 'FSNBTC', 'FSNETH', 'FSNUSD', 'FUNBTC', 'FUNETH', 'FUNUSD', 'GNTBTC', 'GNTETH', 'GNTUSD', 'GOTETH', 'GOTEUR', 'GOTUSD', 'HOTBTC', 'HOTETH', 'HOTUSD', 'IOSBTC', 'IOSETH', 'IOSUSD', 'IOTBTC', 'IOTETH', 'IOTEUR', 'IOTGBP', 'IOTJPY', 'IOTUSD', 'IQXBTC', 'IQXEOS', 'IQXUSD', 'KNCBTC', 'KNCUSD', 'LRCBTC', 'LRCUSD', 'LTCBTC', 'LTCUSD', 'LYMBTC', 'LYMETH', 'LYMUSD', 'MANETH', 'MANUSD', 'MITBTC', 'MITETH', 'MITUSD', 'MKRBTC', 'MKRETH', 'MKRUSD', 'MNABTC', 'MNAETH', 'MNAUSD', 'MTNBTC', 'MTNETH', 'MTNUSD', 'NCABTC', 'NCAUSD', 'NEOBTC', 'NEOETH', 'NEOEUR', 'NEOGBP', 'NEOJPY', 'NEOUSD', 'NIOETH', 'NIOUSD', 'ODEBTC', 'ODEETH', 'ODEUSD', 'OMGBTC', 'OMGETH', 'OMGUSD', 'ORSBTC', 'ORSUSD', 'PAIBTC', 'PAIUSD', 'POABTC', 'POAETH', 'POAUSD', 'POYBTC', 'POYETH', 'POYUSD', 'QSHBTC', 'QSHETH', 'QSHUSD', 'QTMBTC', 'QTMETH', 'QTMUSD', 'RCNBTC', 'RCNETH', 'RCNUSD', 'RDNBTC', 'RDNETH', 'RDNUSD', 'REPBTC', 'REPETH', 'REPUSD', 'REQBTC', 'REQETH', 'REQUSD', 'RLCBTC', 'RLCETH', 'RLCUSD', 'RRTBTC', 'RRTUSD', 'SANBTC', 'SANETH', 'SANUSD', 'SEEBTC', 'SEEETH', 'SEEUSD', 'SENBTC', 'SENETH', 'SENUSD', 'SNGBTC', 'SNGETH', 'SNGUSD', 'SNTBTC', 'SNTETH', 'SNTUSD', 'SPKBTC', 'SPKETH', 'SPKUSD', 'STJETH', 'STJUSD', 'TKNETH', 'TKNUSD', 'TNBBTC', 'TNBETH', 'TNBUSD', 'TRXBTC', 'TRXETH', 'TRXUSD', 'UTKBTC', 'UTKUSD', 'UTNETH', 'UTNUSD', 'VEEBTC', 'VEEETH', 'VEEUSD', 'VETBTC', 'VETETH', 'VETUSD', 'WAXBTC', 'WAXETH', 'WAXUSD', 'WPRUSD', 'XLMBTC', 'XLMETH', 'XLMEUR', 'XLMGBP', 'XLMJPY', 'XLMUSD', 'XMRBTC', 'XMRUSD', 'XRAETH', 'XRPBTC', 'XRPUSD', 'XVGBTC', 'XVGETH', 'XVGEUR', 'XVGGBP', 'XVGJPY', 'XVGUSD', 'YYWBTC', 'YYWETH', 'YYWUSD', 'ZCNBTC', 'ZCNETH', 'ZCNUSD', 'ZECBTC', 'ZECUSD', 'ZILBTC', 'ZILETH', 'ZILUSD', 'ZRXBTC', 'ZRXETH', 'ZRXUSD']
end_path = 'E:\\BaiduNetdiskDownload\\bitfinex_20180401_20180927\\'

file_path = 'E:\\BaiduNetdiskDownload\\bitfinex_20180401_20180927_all\\'
# for dirpath in os.listdir(file_path):
#     path = os.path.join(file_path, dirpath)
#     l = os.listdir(path)
#     print(l)
#
# for i in symbol_list:
#     path = end_path.format(i)
#     file_name = path + '\\BITFINEX_20180401_20180927_{}.csv'
#     print(file_name)
    # for f in os.listdir(file_path):
    #     f_path = os.path.join(file_path, f)
    #     for data_f in os.listdir(f_path):
    #         if data_f == i:
    #             data_f_path = os.path.join(f_path, data_f)
    #             for j in os.listdir(data_f_path):
    #                 print(j)

# for i in symbol_list:
#     os.mkdir(end_path.format(i))
#     for j in ['1T','5T','15T', '30T', '1H']:
#         os.mkdir(end_path.format(i) + '\\{}'.format(j))

print()
###############  统一转移文件 ###################
# for dirpath, dirnames, filenames in os.walk(file_path):
#     f_name = dirpath.split('\\')[-1]
#     print(f_name)
#     h_f = []
#     for i in symbol_list:
#
#         path = end_path.format(i)
#         file_name = path + '\\BITFINEX_{}_20180401_20180927_{}.csv'
#         if i == f_name:
#             print('xiangtong')
#             for filepath in filenames:
#                 file_path = dirpath + '\\'+ filepath
#                 print(file_path)
#                 for j in ['1T', '5T', '15T', '30T', '1H']:
#
#                     if '_{}'.format(j) in file_path:
#                         new_path = path + '\\{}\\'.format(j)
#                         isExists = os.path.exists(new_path + '\\{}'.format(file_path.split('\\')[-1]))
#                         if not isExists:
#                             shutil.copy(file_path, new_path + '\\{}'.format(file_path.split('\\')[-1]))
#                         else:
#                             print('存在该文件')
#

###################   汇总数据 ##################
# for i in symbol_list:
#     os.mkdir(file_path.format(i))
#     for j in ['1T', '5T', '15T', '30T', '1H']:
#         os.mkdir(file_path.format(i) + '\\{}'.format(j))

# for i in symbol_list:
#     fOld_path = end_path + '{}\\'.format(i)
#     for t in ['1T', '5T', '15T', '30T', '1H']:
#         ffOld_p = fOld_path + '{}\\'.format(t)
#         df_list = []
#
#         for j in os.listdir(ffOld_p):
#             path = os.path.join(ffOld_p, j)
#             print(path)
#             df = pd.read_csv(path, header=1, index_col=0)
#             df_list.append(df)
#         df1 = pd.DataFrame()
#         result = df1.append(df_list)
#         print(result)
#         pp = 'BITFINEX_{}_20180401_20180917_{}.csv'.format(i, t)
#         w_path = file_path + '{}\\{}\\{}'.format(i, t, pp)
#         print(w_path)
#         result.to_csv(w_path)
# import matplotlib.dates as mdate
# _f = '/Users/billy/PycharmProjects/BackTest/BackTest_v1/outputData/2017-07-01_2017-07-02_balance_2.csv'
# data = pd.read_csv(_f)
# print(data)
# fig = plt.figure()
# ax = fig.add_subplot(111)
# # data['time'] = pd.to_datetime(data['time'])
# # ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d %H:%M:%S'))
# plt.plot(data.index, data['data_price'])
# # print(pd.date_range(data.index[0],data.index[-1]))
# # plt.xticks(pd.date_range(data.index[0],data.index[-1]),rotation=45)
#
# plt.show()

