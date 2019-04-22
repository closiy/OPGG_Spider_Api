import requests
import chardet
import pymongo
import spider_single_champion_data
from bs4 import BeautifulSoup

# split url to get counter champions id
def get_champion_id_from_url(data_champion_counter_url):
    return data_champion_counter_url.split('/')[-1].split('.')[0].lower()

def pos_changeto_id(pos):

    '''
    change position text to url position id
    :param pos:
    :return:
    '''

    if pos == 'Middle':
        return 'mid'
    if pos == 'Jungle':
        return 'jungle'
    if pos == 'Support':
        return 'support'
    if pos == 'Top':
        return 'top'
    if pos == 'Bottom':
        return 'bot'


if __name__ == '__main__':
    # get champions name and url
    # connect to mongodb
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['demacia_db']
    mycol = mydb['champions']
    url = 'https://www.op.gg/champion/statistics'
    r1 = requests.get(url)
    r1.encoding = chardet.detect(r1.content)["encoding"]
    soup = BeautifulSoup(r1.text, 'html.parser')
    for content in soup.find_all(name='div', class_='champion-index__champion-list'):
        for champions in content.find_all(name='div', attrs={'data-champion-key': True}):
            # print key: data-champion-key

            # print(champions.attrs['data-champion-key'], end=" ")
            a_list = champions.find_all(name='a', attrs={'href':True})
            for a in a_list:
                url = 'https://www.op.gg' + a.attrs['href']
                # save datas to Collection in champions of demacia_db in localhost
                champion_key = {'data_champion_key': champions.attrs['data-champion-key']}  # champion ID
                a_pos = a.find_all(name='div', class_='champion-index__champion-item__position')
                print(champion_key)
                for a_pos_i in a_pos:
                    pos = a_pos_i.find(name='span')
                    pos_url = url + '/' + pos_changeto_id(pos.text)
                    champion_pos_text = {'data_champion_pos_text': pos.text}  # champion position names such as Middle
                    champion_pos_id = {'data_champion_pos_id': pos_changeto_id(pos.text)}  # champion position ID such as mid
                    champion_pos_url = {'data_champion_pos_url': pos_url}
                    '''
                    insert data
                    '''
                    mydict = {'data_champion_key': champions.attrs['data-champion-key'],
                              'data_champion_pos_text': champion_pos_text['data_champion_pos_text'],
                              'data_champion_pos_id': champion_pos_id['data_champion_pos_id'],
                              'data_champion_pos_url': champion_pos_url['data_champion_pos_url'],
                              }
                    mycol.insert_one(mydict)
                    spider_single_champion_data.get_champions_data(champion_pos_url['data_champion_pos_url'], champions.attrs['data-champion-key'], mycol)
                    print('insert', mydict)
