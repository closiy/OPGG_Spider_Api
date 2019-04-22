import pymongo
import get_single_champion_data

if __name__ == '__main__':
    # connect to mongodb
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['demacia_db']
    mycol = mydb['champions']

    data_champion_list = mycol.find({'data_champion_key': {'$exists': True}})
    tmp = ''
    for i in data_champion_list:
        # tmp use to remove duplicates
        if i['data_champion_key'] != tmp:
            # use module get_single_champion_data's function get_single_champion_mongodb_data and save as json
            get_single_champion_data.get_single_champion_mongodb_data(i['data_champion_key'])
        tmp = i['data_champion_key']