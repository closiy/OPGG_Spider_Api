#!/usr/bin/python3
import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['demacia_db']
mycol = mydb['champions']
# mydict = {'name':'closiy', 'alexa':'10000', 'url':'https://baidu.com'}

champion_key = {'data-champion-key': 'yorick'}
new_url = 'https://www.op.gg/champion/yorick/statistics'
mydoc = mycol.find_one(champion_key)
if mydoc:
    old_query = {'url': mydoc['url']}
    update_query = {'$set': {'url': new_url}}
    mycol.update_one(old_query, update_query)
    print(mydoc)
else:
    print("not exit")
