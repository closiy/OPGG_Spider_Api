#!/usr/bin/python3
import requests
import chardet
import pymongo
import json
from bs4 import BeautifulSoup

def get_champion_id_from_url(data_champion_counter_url):
    return data_champion_counter_url.split('/')[-1].split('.')[0].lower()

def get_champions_information_postion(data_champions_ranking_pos):
    data_champions_ranking_pos = data_champions_ranking_pos.replace('\n', '').replace('\t', '').replace(' ', '').lower()
    data_champions_ranking_pos = data_champions_ranking_pos.split(',')
    return data_champions_ranking_pos

def get_champions_ranking_overview(tbody_pos_ranking, mycol, pos_ranking):
    '''
    get overview list of champions ranking
    :param tobdy_pos_ranking:
    :return:
    '''
    data_champions_ranking_list = []
    champions_list = []
    for item in tbody_pos_ranking.find_all(name='tr'):
        data_champions_ranking_num = item.find(name='td', class_='champion-index-table__cell champion-index-table__cell--rank').text
        data_champions_ranking_url = 'https://www.op.gg' + item.find(name='a').attrs['href']
        data_champions_ranking_name = item.find(name='div', class_='champion-index-table__name').text.lower()
        tmp_champions_name = item.find(name='div', class_='champion-index-table__name').text
        tmp_champions_name = ''.join([x for x in tmp_champions_name if x.isalpha()])
        if tmp_champions_name == 'Wukong':
            tmp_champions_name = 'MonkeyKing'
        if tmp_champions_name =='NunuWillump':
            tmp_champions_name = 'Nunu'
        data_champions_ranking_img = 'https://opgg-static.akamaized.net/images/lol/champion/'+ tmp_champions_name +'.png?image=w_140&v=1'
        data_champions_ranking_pos = item.find(name='div', class_='champion-index-table__position').text
        data_champions_ranking_pos = get_champions_information_postion(data_champions_ranking_pos)
        j = 1
        for td_rate in item.find_all(name='td', class_='champion-index-table__cell champion-index-table__cell--value', limit=3):

            if j == 1:
                rate = float(td_rate.text.replace('\n', '').replace('\t', '').replace(' ', '').split('%')[0])
                data_champions_ranking_winrate = rate
            elif j ==2:
                rate = float(td_rate.text.replace('\n', '').replace('\t', '').replace(' ', '').split('%')[0])
                data_champions_ranking_pick = rate
            else:
                data_champions_ranking_tier = td_rate.find(name='img')['src'].split('/')[-1].split('-')[-1].split('.')[0]
            j += 1
        # winrate = item.find(name='td', class_='champion-index-table__cell champion-index-table__cell--value').text
        # data_champions_ranking_winrate = float(winrate.split('%')[0])
        # pickrate = item.find_next(name='td', class_='champion-index-table__cell champion-index-table__cell--value').text
        # data_champions_ranking_pick = float(pickrate.split('%')[0])
        data_champions_ranking_list += [{
            'data_champion_ranking_name': data_champions_ranking_name,
            'data_champion_ranking_num': data_champions_ranking_num,
            'data_champion_ranking_url': data_champions_ranking_url,
            'data_champion_ranking_img': data_champions_ranking_img,
            'data_champion_ranking_pos': data_champions_ranking_pos,
            'data_champion_ranking_winrate': data_champions_ranking_winrate,
            'data_champion_ranking_pick': data_champions_ranking_pick,
            'data_champions_ranking_tier':data_champions_ranking_tier
        }]

    champions_ranking_json = json.dumps(data_champions_ranking_list)
    system_version = 'windows'
    if system_version == 'linux':
        json_file_name = '/home/www/htdocs/wp-content/uploads/' + pos_ranking + '.json'
        with open(json_file_name, 'w') as json_file_obj:
            json.dump(data_champions_ranking_list, json_file_obj)
    else:
        json_file_name = 'E:/data/' + pos_ranking + '.json'
        with open(json_file_name, 'w') as json_file_obj:
            json.dump(data_champions_ranking_list, json_file_obj)

    # print(champions_ranking_json)
    if mycol.find():
        mycol.drop()
        mycol.insert(data_champions_ranking_list)
        print('update success!')
    else:
        mycol.insert(data_champions_ranking_list)
        print("insert success!")


def get_champions_rankings(data_champions_ranking_url, mydb):
    r2 = requests.get(data_champions_ranking_url)
    r2.encoding = chardet.detect(r2.content)["encoding"]
    soup2 = BeautifulSoup(r2.text, 'html.parser')
    table_champions_ranking = soup2.find(name='table', class_='champion-index-table tabItems')
    tbody_top_ranking = table_champions_ranking.find(name='tbody', class_='tabItem champion-trend-tier-TOP')
    tbody_jugle_ranking = table_champions_ranking.find(name='tbody', class_='tabItem champion-trend-tier-JUNGLE')
    tbody_mid_ranking = table_champions_ranking.find(name='tbody', class_='tabItem champion-trend-tier-MID')
    tbody_mid_ranking = table_champions_ranking.find(name='tbody', class_='tabItem champion-trend-tier-MID')
    tbody_adc_ranking = table_champions_ranking.find(name='tbody', class_='tabItem champion-trend-tier-ADC')
    tbody_support_ranking = table_champions_ranking.find(name='tbody', class_='tabItem champion-trend-tier-SUPPORT')
    mycol = mydb['champions_ranking_top']
    get_champions_ranking_overview(tbody_top_ranking, mycol, 'top_ranking')
    mycol = mydb['champions_ranking_jugle']
    get_champions_ranking_overview(tbody_jugle_ranking, mycol, 'jungle_ranking')
    mycol = mydb['champions_ranking_mid']
    get_champions_ranking_overview(tbody_mid_ranking, mycol, 'mid_ranking')
    mycol = mydb['champions_ranking_adc']
    get_champions_ranking_overview(tbody_adc_ranking, mycol, 'adc_ranking')
    mycol = mydb['champions_ranking_support']
    get_champions_ranking_overview(tbody_support_ranking, mycol, 'support_ranking')



if __name__ == '__main__':
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['demacia_db']
    data_champions_ranking_url = 'https://www.op.gg/champion/statistics'
    get_champions_rankings(data_champions_ranking_url, mydb)



