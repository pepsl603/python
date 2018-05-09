import pandas as pd
from pymongo import MongoClient
import datetime
import pprint
import time
import pandas as pd
# import numpy as np
# import cx_Oracle
import json

conn = MongoClient('192.168.235.128', 27017)
db = conn.mytest
ports = db.ocfport
# ports.delete_many({})

# reader = pd.read_csv(r"F:\data\PORT_OCFPORT_F_JM.CSV", sep=',', iterator = True, error_bad_lines=False,
#                      warn_bad_lines=False)
# ,usecols=[0, 1, 2]

begintime = datetime.datetime.now()

print("开始统计:", begintime)
# print("开始写库:", begintime)
# while True:
#     try:
#         df = reader.get_chunk(1000000)
#         ports.insert_many(json.loads(df.T.to_json()).values())
#         # break
#     except:
#         break

print("空闲端口有：", ports.find({"业务状态": "'空闲'"}).count())

endtime = datetime.datetime.now()
# print("完成写库{}条:{}".format(ports.count(), endtime))
print('耗时：', endtime-begintime)
conn.close()


