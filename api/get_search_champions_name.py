import pymongo
import  json

def get_champions_name(mycol):
    data = mycol.find({},{"data_champion_key": 1, "data_champion_pos_id":1 , "_id":0})
    champions_name =[]
    flag = {'data_champion_key': ''}
    for item in data:
        if flag['data_champion_key'] != item['data_champion_key']:
            champions_name +=[item['data_champion_key']+'_'+item["data_champion_pos_id"]]
            flag = item
    json_data = {'champions_name':champions_name}

    system_version = 'windows'
    if system_version == 'linux':
        json_file_name = '/home/www/htdocs/wp-content/uploads/' + 'search_champion_name.json'
        with open(json_file_name, 'w') as json_file_obj:
            json.dump(json_data, json_file_obj)
    else:
        json_file_name = 'E:/data/' + 'search_champion_name.json'
        with open(json_file_name, 'w') as json_file_obj:
            json.dump(json_data, json_file_obj)


if __name__ == '__main__':
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['demacia_db']
    mycol = mydb['champions']
    get_champions_name(mycol)