import pandas
import datetime
import pymysql
from sqlalchemy import create_engine
import configparser
import logging

# 记录日志的需求
logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(message)s', datefmt='%Y-%m-%d')
logging.info('调试测试')
# 读取配置文件，方便在工作环境或者家里使用
myConfig = configparser.ConfigParser()

# 此处要根据实际使用环境选择设置公司环境还是家里环境配置文件，公司是“read_excel_company.config”，家里是”read_excel_home.config“
myConfig.read('read_excel_company.config')

db_host = myConfig.get('db', 'db_host')
db_port = myConfig.get('db', 'db_port')
db_user = myConfig.get('db', 'db_user')
db_pass = myConfig.get('db', 'db_pass')
db_name = myConfig.get('db', 'db_name')


# 连接到本地的mysql数据库
mysqlConn = create_engine(
    "mysql+pymysql://" + db_user + ":" + db_pass + "@" + db_host + ":" + db_port + "/liangwh?charset=utf8")





# 导入水星数据到mysql
def load_from_excel(str_file_name, table_name):
    # 记录开始运行时间，程序结束前再打印时间，计算时间差
    startTime = datetime.datetime.now()
    logging.info('导入并保存资料启动时间：' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # 从Excel文件中导入客户资料，其中数值类型的字段在导入前请使用excel软件进行转换为数值型
    data_from_excel = pandas.read_excel(str_file_name,
                                   dtype=str
                                   )
    print(data_from_excel.dtypes)

    # 把从excel导入的数据保存到mysql中
    data_from_excel.to_sql(table_name, mysqlConn, schema=db_name, if_exists="append", index=False, index_label=False)

    logging.info('导入并保存资料结束时间：' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    logging.info('－－－－－－－－－－－－－－－－－－－－－－－－－－－')
    logging.info('导入并保存资料结束，运行时间为：' + str(datetime.datetime.now() - startTime))



# 读取mysql上的数据
def read_from_mysql(table_name):
    # 查询语句，选出employee表中的所有数据
    sql = '''select * from %s''' % (table_name)
    # read_sql_query的两个参数: sql语句， 数据库连接
    df_from_sql = pandas.read_sql_query(sql, mysqlConn)

    df_increase_range = pandas.Series(list(df_from_sql['收盘']), index=pandas.to_datetime(df_from_sql['时间']))
    df_count_result=(df_increase_range - df_increase_range.shift(1)) / df_increase_range.shift(1)



    # 输出employee表的查询结果
    #print(df_from_sql)

# 导入对应统计年和月份的客户数据
#load_from_excel(r"601138.xlsx",'601138')
read_from_mysql('s601138')
