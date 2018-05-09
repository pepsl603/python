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

reader = pd.read_csv(r"F:\data\PORT_OCFPORT_F_JM.CSV", sep=',', iterator = True, error_bad_lines=False, warn_bad_lines=False)

df = reader.get_chunk(15)

print('开始写文件:', getNowTime())
df.to_csv('test.csv', index=False, mode='w')
print('结束写文件:', getNowTime())