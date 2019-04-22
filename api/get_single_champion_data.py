#!/usr/bin/python3
import json
import pymongo

def get_single_champion_mongodb_data(data_champion_id):
    # connect to mongodb
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['demacia_db']
    mycol = mydb['champions']
    # system version
    system_version = 'windows'

    data_champion_stats = mycol.find({'data_champion_key': data_champion_id})
    for data_champion in data_champion_stats:
        del data_champion['_id']
        champion_pos_name = data_champion['data_champion_pos_id']
        champion_name = data_champion['data_champion_key']
        if system_version == 'linux':
            json_file_name = '/home/www/htdocs/wp-content/uploads/' + champion_name + '_' + champion_pos_name + '.json'
            with open(json_file_name, 'w') as json_file_obj:
                json.dump(data_champion, json_file_obj)
        else:
            json_file_name = 'E:/data/' + champion_name + '_' + champion_pos_name + '.json'
            with open(json_file_name, 'w') as json_file_obj:
                json.dump(data_champion, json_file_obj)
        print(data_champion)

if __name__ == '__main__':
    data_champion_id = 'zyra'
    get_single_champion_mongodb_data(data_champion_id)