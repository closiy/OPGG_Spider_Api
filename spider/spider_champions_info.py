import requests
import chardet
import pymongo
from bs4 import BeautifulSoup



def get_champions_data(url, data_champion_key ):
    '''
    :param url:
    :param data_champion_key:
    :return:
    '''
    r2 = requests.get(url)
    r2.encoding = chardet.detect(r2.content)["encoding"]
    soup2 = BeautifulSoup(r2.text, 'html.parser')
    '''
    header static reduce
    '''
    header = soup2.find_all(name='div', attrs=['class', 'l-champion-statistics-header'])
    print(header)

    '''
    tabWrap _recognized
    reduce data static
    
    '''

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
                champion_key = {'data-champion-key': champions.attrs['data-champion-key']}  # champion ID
                a_pos = a.find_all(name='div', class_='champion-index__champion-item__position')
                print(champion_key)
                for a_pos_i in a_pos:
                    pos = a_pos_i.find(name='span')
                    pos_url = url + '/' + pos_changeto_id(pos.text)
                    champion_pos_text = {'data-champion-pos-text': pos.text}  # champion position names such as Middle
                    champion_pos_id = {'data-champion-pos-id': pos_changeto_id(pos.text)}  # champion position ID such as mid
                    champion_pos_url = {'data-champion-pos-url': pos_url}
                    '''
                    insert data
                    '''
                    mydict = {'data-champion-key': champions.attrs['data-champion-key'],
                              'data-champion-pos-text': champion_pos_text['data-champion-pos-text'],
                              'data-champion-pos-id': champion_pos_id['data-champion-pos-id'],
                              'data-champion-pos-url': champion_pos_url['data-champion-pos-url'],
                              }
                    mycol.insert_one(mydict)
                    print('insert', mydict)
