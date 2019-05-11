import pymongo
import json

def get_random_champion_data(mycol):
    data=  mycol.aggregate(
        [
            {"$sample": {"size": 1}}
        ]
    )
    random_champion = {}
    for item in data:
        del item['_id']
        random_champion = item
    system_version = 'windows'
    if system_version == 'linux':
        json_file_name = '/home/www/htdocs/wp-content/uploads/' + 'random_champion.json'
        with open(json_file_name, 'w') as json_file_obj:
            json.dump(random_champion, json_file_obj)
    else:
        json_file_name = 'E:/data/' + 'random_champion.json'
        with open(json_file_name, 'w') as json_file_obj:
            json.dump(random_champion, json_file_obj)


if __name__ == '__main__':
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['demacia_db']
    mycol = mydb['champions']
    get_random_champion_data(mycol)
