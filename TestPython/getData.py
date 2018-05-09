# import csv
# import pandas

# with open('D:\数据库\SRS_FUL_IRMS.Resource.ALL.ZZ_20180328005323\DEVICE_IMS_VOLTE_ATCF_F.CSV',encoding='utf-8') as f:
#     datareader = csv.reader(f);
#     print (list(datareader))

import time
import pandas as pd
import numpy as np
import cx_Oracle

#返回当前时间
def getNowTime():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)
    return time_stamp

reader = pd.read_csv(r"F:\data\PORT_OCFPORT_F_JM.CSV", sep=',', iterator = True, error_bad_lines=False, warn_bad_lines=False,
                     usecols=[0,1,2])

df = reader.get_chunk(5000000)
# print(np.array(df[:]).tolist())
#
# print('开始写文件:', getNowTime())
# df.to_csv('test.csv', index=False, mode='w')
# print('结束写文件:', getNowTime())

print('开始连接数据库:', getNowTime())
db = cx_Oracle.connect('pipesys', 'pipesys', '192.168.1.129:1521/orcl01')
print('数据库连接成功:', getNowTime())
cr = db.cursor()
print('删除表数据:', getNowTime())
dsql = "truncate table AM_PORT_OCFPORT_F"
print('删除完成:', getNowTime())
print('开始写库:', getNowTime())
cr.execute(dsql)
sql = "INSERT INTO AM_PORT_OCFPORT_F(OUTID, PORTCODE,BUSISTATUS) VALUES (:1, :2 ,:3)"
cr.prepare(sql)
cr.executemany(None, np.array(df[:]).tolist())
db.commit()
print('写库结束:', getNowTime())
db.close()
# try:
#     # df = reader.get_chunk(204)
#     print('开始读取CSV文件:', getNowTime())
#     df = reader.get_chunk(10)
#     print('结束读取CSV:', getNowTime())
#
#     print('开始写文件:', getNowTime())
#     df.to_csv('test.csv', index=False, mode='w')
#     print('结束写文件:', getNowTime())
#
# except StopIteration:
#     print("Iteration is stopped.")

# chunk = chunks.get_chunk(1)
# print(chunk)

# reader = pd.read_csv('F:\data\SRS_FUL_IRMS.Resource.ALL.ZZ_20180328005323\DEVICE_IMS_VOLTE_ATCF_F.CSV',
#                      encoding='utf-8', sep=',')

# try:
#     df = reader.get_chunk(100000000)
# except StopIteration:
#     print("Iteration is stopped.")

# loop = True
# chunkSize = 100000
# chunks = []
# while loop:
#     try:
#         chunk = reader.get_chunk(chunkSize)
#         chunks.append(chunk)
#     except StopIteration:
#         loop = False
#         print("Iteration is stopped.")
# df = pd.concat(chunks, ignore_index=True)