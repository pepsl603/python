from pymongo import MongoClient
import datetime
import pprint

conn = MongoClient('192.168.235.128', 27017)
db = conn.mytest

my_set = db.test_set

user = {"name":"陈二", "age":32, "recdate": datetime.datetime.now()}

dbusers = db.users
userid = dbusers.insert_one(user).inserted_id
print(userid)

users = [{"name": "陈二", "age": 32, "recdate": datetime.datetime.now()},
         {"name": "张三", "age": 23, "recdate": datetime.datetime.now()},
         {"name": "李四", "age": 55, "recdate": datetime.datetime.now()}]

userids = dbusers.insert_many(users)

user = dbusers.find_one()
print(user)
user = dbusers.find_one()
pprint.pprint(user)

for user in dbusers.find({"name":"陈二"}):
    pprint.pprint(user)
print('名字叫陈二的人有{}个！'.format(dbusers.find({"name":"陈二"}).count()))
