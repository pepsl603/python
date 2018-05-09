# age = 20
# name = 'Swaroop'
# print('{0} was {1} years old when he wrote this book'.format(name, age))
# print("Why is {0} playing with that python?".format(name))
# print('{0:.3f}'.format(1.0/3),end='*****\n')
# print('{0:x^11}'.format('hello'))
# print(r'What\'s your name? \t \t ddd')
# i=5
# print(i)
# print(22)
# guess = int(input('Enter an integer : '))
# if guess>5:
#     print('大于5')
#     print(guess)
# else:
#     print('xxxx')
#
# for x in range(1,3):
#     print(x)
# else:
#     print("over!")


# def total(a=5, *numbers, **phonebook):
#     '''
#
#     :param a:
#     :param numbers:
#     :param phonebook:
#     :return:
#     '''
#     print('a', a)
# #遍历元组中的所有项目
#     for single_item in numbers:
#         print('single_item', single_item)
# #遍历字典中的所有项目
#     for first_part, second_part in phonebook.items():
#         print(first_part,second_part)
#
# print(total.__doc__)


# import  sys
# import os
# import Tool
# from Tool import getBig

# a = 1
# print(getBig(4,2))
# print(Tool.__version__)
# print(dir())

#列表
# numberlist = [9,2,8,4]
# print(len(numberlist))
# numberlist.append(5)
# print(numberlist)
# numberlist.append(6)
# print(numberlist)
# numberlist.sort()
# print(numberlist)
# del numberlist[3]
# print(numberlist)

#元组
# zoo = ('python','c++','java')
# new_zoo = 'c#', 'swift', 'js'
# print(zoo)
# print(new_zoo[1][1])
# print(len(new_zoo))
# print(len(new_zoo[1]))

#字典
# ab = {'x': 111, 'y': 222, 'z': 333}
# print(ab)
# print(ab['x'])
# ab['J'] = 11
# del ab["x"]
# print(ab)
#
# for key,value in ab.items():
#     print('key is {} ,value is {}'.format(key,value))
# keyinput = input('请输入：')
# if keyinput in ab:
#     print('存在')

# ablist = (['1','2','3'],['x','y'])
# print(ablist[0][::-1])

# print(Tool.reverse('abcde'))
#
# f = open('test.txt', 'a')
# f.write('\n你好，写文件')
# f.close()
#
# f = open('test.txt')
# while True:
#     line = f.readline()
#     if len(line) == 0:
#         break
#     print(line, end=' ')
# f.close()

# import pickle
# shoplistfile= 'test.data'
# shoplist = ['apple', '酒', '花生米']
#
# f = open(shoplistfile, 'wb')
# pickle.dump(shoplist, f)
# f.close()
# del shoplist
#
# f = open(shoplistfile, 'rb')
# sorelist = pickle.load(f)
# print(sorelist)
# f.close()


# import sys
# import time
# f = None
# try:
#     f = open("nginx.conf")
# # 我们常用的文件阅读风格
#     while True:
#         line = f.readline()
#         if len(line) == 0:
#             break
#         print(line, end='')
#         # sys.stdout.flush()
#         # print("Press ctrl+c now")
# # 为了确保它能运行一段时间
#         time.sleep(2)
# except IOError:
#     print("Could not find file poem.txt")
# except KeyboardInterrupt:
#     print("!! You cancelled the reading from the file.")
# finally:
#     if f:
#         f.close()
# print("(Cleaning up: Closed the file)")

#
# import os
# import platform
# import logging
# if platform.platform().startswith('Windows'):
#     logging_file = os.path.join(os.getenv('HOMEDRIVE'),os.getenv('HOMEPATH'),'test.log')
#     print(os.getenv('HOMEDRIVE'))
#     print(os.getenv('HOMEPATH'))
# else:
#     logging_file = os.path.join(os.getenv('HOME'),'test.log')
# print("Logging to", logging_file)
#
#
# # logging.basicConfig(level=logging.DEBUG,
# #                     format='%(asctime)s : %(levelname)s : %(message)s',
# #                     filename=logging_file,
# #                     filemode='a',)
# logging.basicConfig(level=logging.DEBUG,
#                     format='【%(levelname)s】 %(asctime)s \n %(message)s\n',
#                     filename=logging_file,
#                     filemode='a',)
# logging.debug("start debug")
# logging.info("do info")
# logging.warning("waring now")


import pandas as pd

import cx_Oracle

# db = cx_Oracle.connect('pipesys', 'pipesys', '192.168.1.129:1521/orcl01')
# print(db.version)
# cr = db.cursor()
# sql = 'select userid,username from sys_users'
# cr.execute(sql)
# rs = cr.fetchall()
# zz = pd.DataFrame(rs)
# print(zz)
#
# db.close()
#
from sqlalchemy import create_engine
from sqlalchemy.sql.sqltypes import *

engine = create_engine('oracle+cx_oracle://pipesys:pipesys@192.168.1.129:1521/orcl01')

df = pd.DataFrame([[1, 'xxx', 'aaa'], [2, 'yyy', 'bbb']], columns=list('abc'))
# conn = cx_Oracle.connect('pipesys', 'pipesys', '192.168.1.129:1521/orcl01')
coltype = {"a": int, "b": VARCHAR(200), "C": VARCHAR(200)}
df.to_sql('testdbtable', engine, if_exists='replace', index='False', dtype=coltype)
# conn.close()
print("finish load db")

