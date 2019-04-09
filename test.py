#!/usr/bin/python3
import requests
import chardet
import pymongo
from bs4 import BeautifulSoup

# split url to get counter champions id
def get_champion_id_from_url(data_champion_counter_url):
    return data_champion_counter_url.split('/')[-1].split('.')[0].lower()

def get_champions_data(data_champion_pos_url, data_champion_key, mycol):
    '''
    get champion data in it's position
    :param data_champion_pos_url:
    :param data_champion_key:
    :return:
    '''
    r2 = requests.get(data_champion_pos_url)
    r2.encoding = chardet.detect(r2.content)["encoding"]
    soup2 = BeautifulSoup(r2.text, 'html.parser')
    champion_flag = {'data-champion-pos-url': data_champion_pos_url}  # flag of champion, to find out data

    '''
    get header info from OPGG champions page
    '''
    # header of pages, data-type as  position_role position_rate
    header = soup2.find(name='div', attrs=['class', 'l-champion-statistics-header'])
    li_position = header.find(name='li', class_= 'champion-stats-header__position champion-stats-header__position--active')

    # get and update information of rate
    rate_span = li_position.find(name='span', attrs=['class', 'champion-stats-header__position__rate'])
    champion_pos_rate = {'data-champion-pos-rate': rate_span.text}
    mycol.update_one(champion_flag, {'$set': {'data-champion-pos-rate': champion_pos_rate['data-champion-pos-rate']}})

    # get and update img of champion
    div_img = header.find(name='div', class_='champion-stats-header-info__image')
    champion_img = div_img.find(name='img')
    data_champion_img_url = 'https:' + champion_img.attrs['src']
    mycol.update_one(champion_flag, {'$set': {'data-champion-img-url': data_champion_img_url}})

    # get and update tier of champion
    div_tier = header.find(name='div', class_='champion-stats-header-info__tier')
    champion_tier = div_tier.find(name='b')
    data_champion_tier = champion_tier.text
    mycol.update_one(champion_flag, {'$set': {'data-champion-tier': data_champion_tier}})

    # get and update counter champion
    table_counter = header.find(name='table', class_='champion-stats-header-matchup__table champion-stats-header-matchup__table--strong tabItem')
    data_champion_counter_list = []
    i = 1
    for tr_counter in table_counter.find_all(name='tr'):
        data_champion_counter_url = 'https:' + tr_counter.find(name='img')['src']
        data_champion_counter_winrate = tr_counter.find(name='b').text
        data_champion_counter_id = get_champion_id_from_url(data_champion_counter_url)
        data_champion_counter_list += [{
            'data-champion-counter-id' + str(i): data_champion_counter_id,
            'data-champion-counter-url-' + str(i): data_champion_counter_url,
            'data-champion-counter-winrate-' + str(i): data_champion_counter_winrate}]
        i += 1
    mycol.update_one(champion_flag, {'$set': {'data-champion-counter-list': data_champion_counter_list}})

    # get and update anti-counter champion
    table_anticounter = header.find(name='table',
                                class_='champion-stats-header-matchup__table champion-stats-header-matchup__table--weak tabItem')
    data_champion_anticounter_list = []
    i = 1
    for tr_anticounter in table_anticounter.find_all(name='tr'):
        data_champion_anticounter_url = 'https:' + tr_anticounter.find(name='img')['src']
        data_champion_anticounter_winrate = tr_anticounter.find(name='b').text
        data_champion_anticounter_id = get_champion_id_from_url(data_champion_anticounter_url)
        data_champion_anticounter_list += [{
            'data-champion-anticounter-id' + str(i): data_champion_anticounter_id,
            'data-champion-anticounter-url-' + str(i): data_champion_anticounter_url,
            'data-champion-anticounter-winrate-' + str(i): data_champion_anticounter_winrate}]
        i += 1
    mycol.update_one(champion_flag, {'$set': {'data-champion-anticounter-list': data_champion_anticounter_list}})
    # output data
    print(mycol.find_one(champion_flag))



if __name__ == '__main__':
    # connect to mongodb
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['demacia_db']
    mycol = mydb['champions']

    # test data of 'neeko'
    data_champion_key = 'neeko'
    data_champion_pos_url = 'https://www.op.gg/champion/neeko/statistics/mid'
    get_champions_data(data_champion_pos_url, data_champion_key, mycol)