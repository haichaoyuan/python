# encoding = utf-8
# pandas，更多例子可以参照http://pandas.pydata.org/pandas-docs/stable/10min.html#min
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xlrd
import xlwt


# date_range
def fun1():
    dates = pd.date_range('20170511', periods=6)
    print(dates)

    # DataFrame,随机生成6行4列数据，索引是日期，行名是A,B,C,D
    df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
    print(df)
    print('=========================================')
    # DataFrame,从集合生成串
    df2 = pd.DataFrame({
        'A': 1,
        'b2': pd.Timestamp('20170511'),
        'C': pd.Series(1, index=list(range(4)), dtype='float32'),
        'D': np.array([3] * 4, dtype='int32'),
        'E': pd.Categorical(["test", "train", "test", "train2"]),
        'F': 'FOO'
    })
    print(df2)
    print('df2.dtypes')
    print(df2.dtypes)
    print(df2.head(2))
    print(df2.tail(2))
    print('df.describe')
    print(df.describe())


def fun2():
    df = pd.DataFrame({'A': ['foo', 'bar', 'foo', 'bar', 'foo', 'bar', 'foo', 'foo'],
                       'B': ['one', 'one', 'two', 'three', 'two', 'two', 'one', 'three'],
                       'C': np.random.randn(8), 'D': np.random.randn(8)})
    print(df)
    print(df.groupby(['A', 'B']).sum())
    print(df.groupby(['A']).sum())


# plot 图表
def fun3_Plotting():
    num = 10
    ts = pd.Series(np.random.randn(num), index=pd.date_range('1/1/2000', periods=num))
    ts = ts.cumsum()
    print(ts)
    ts.plot()
    plt.show()

    df = pd.DataFrame(np.random.randn(num, 4), index=ts.index, columns=['A', 'B', 'C', 'D'])
    df.plot()
    plt.show()


# 数据输入输出
def fun4_data_in_out():
    # write to csv
    num = 10
    ts = pd.Series(np.random.randn(num), index=pd.date_range('1/1/2017', periods=num))
    ts.to_csv('res/foo.csv')
    # read from csv
    ts2 = pd.read_csv('res/foo.csv')
    print(ts2)

    df = pd.DataFrame(np.random.randn(num, num), index=ts.index, columns=[list('ABCDEFGHJK')])
    df.to_excel('res/foo.xls', sheet_name='Sheet1')
    ts3 = pd.read_excel('res/foo.xls', 'Sheet1', index_col=None, na_values=['NA'])
    print('================')
    print(ts3)


def fun5_data2array():
    ts = pd.read_excel('res/foo.xls', 'Sheet1', index_col=None, na_values=['NA'])
    print("=====ts")
    print(ts)
    # print("=====ts['A']")
    # print(ts['A'])
    # print("=====ts[0:3]")
    # print(ts.iloc[0:3])
    # print("=====ts.loc['2017-01-01':'2017-01-02']")
    # print(ts.loc['2017-01-01':'2017-01-02'])

    print("=====")
    array = []
    print("=====len")
    print(len(ts.index))
    print(len(ts))
    print("=====items")
    print(ts.items())
    # 按列显示
    # for seg in ts.items():
    #     print("=====seg")
    #     print(seg)
    #     array.append(seg)
    print("=====keys")
    print(ts.keys())
    print("=====columns,等同keys()")
    print(ts.columns)
    print("=====values")
    print(ts.values)
    print("=====遍历数据")
    for index,row in ts.iterrows():
        print("获取行索引", index,",根据列表名获取数据",row.A,'序号获取数据',row[0])
    # print(array)
    # [('词a', 100),('词b', 90),('词c', 80)]
    # print(ts.loc[:, ['A', 'B']])

fun5_data2array()

