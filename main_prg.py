'''
程序介绍：       测试使用Pandas的时间序列功能
编写时间：       2019年7月6日
编写人：         AdamsLiang

版本：           0.0.1

数据来源：       上证50过去三年的日线数据，取自通达信行情软件的“数据导出”。
'''


import pandas as pd
import datetime

# 从excel中导入过去三年的每日数据
def load_510050_data():
    return pd.read_excel(r"C:\Users\yhlia\Desktop\510050.xlsx")

#生成时间序列列示的数据
def creat_my_series(my_data):
    my_series_data=pd.Series(list(my_data['收盘价']),index=pd.to_datetime(my_data['时间'])) # 此处要注意把数据转换为list类型
    return my_series_data

# 设置数据返回每月的最后一天数值
data_510050=creat_my_series(load_510050_data()).resample('M').first() # resample('M',how='first') # 已经不建议使用，应该使用当前方法

print((data_510050-data_510050.shift(1))/data_510050.shift(1)) #打印出过去三年每个月对比前一个月的涨跌情况