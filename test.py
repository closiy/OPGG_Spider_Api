#!/usr/bin/python3
import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['test']
mycol = mydb['site']
#mydict = {'name':'closiy', 'alexa':'10000', 'url':'https://baidu.com'}

for i in mycol.find():
    print(i)
if mydb:
    print("数据库已存在！")