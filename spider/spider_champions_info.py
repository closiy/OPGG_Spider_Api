import requests
import chardet
import pymongo
from bs4 import BeautifulSoup

# connect to mongodb
myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['demacia_db']
mycol = mydb['champions']


url = 'https://www.op.gg/champion/statistics'
r1 = requests.get(url)
r1.encoding = chardet.detect(r1.content)["encoding"]
soup = BeautifulSoup(r1.text, 'html.parser')


# 获取英雄的 名称 和 对应爬取网址
for content in soup.find_all(name='div', class_='champion-index__champion-list'):
    for champions in content.find_all(name='div', attrs={'data-champion-key': True}):
        # 打印 关键属性 data-champion-key

        # print(champions.attrs['data-champion-key'], end=" ")
        a_list = champions.find_all(name='a', attrs={'href':True})
        for a in a_list:
            url = 'https://www.op.gg' + a.attrs['href']
            # save datas to Collection in champions of demacia_db in localhost

            champion_key = {'data-champion-key': champions.attrs['data-champion-key']}
            mydoc = mycol.find_one(champion_key)
            if mydoc:
                '''
                更新数据
                Update data
                '''
                old_query = {'url': mydoc['url']}
                update_query = {'$set': {'url': url}}
                print('已更新', end=" ")
                print(mydoc)
            else:
                '''
                插入数据
                insert data
                '''
                mydict = {'data-champion-key': champions.attrs['data-champion-key'], 'url': url}
                #mycol.insert_one(mydict)
                print('已插入', mydict)

        # 将获取的数据 存入数据库 或者 保存为 .txt or .json 文件
