import requests
import chardet
from bs4 import BeautifulSoup
import json
# write as .txt
fobj = open('ranking.txt', 'w')

url = 'http://www.op.gg/ranking/ladder/'

'''
according to Page's number to spider summoner's data
range(1,n) n is total number of while you want to spider
'''
data_summoner_ranking_list = []
for page in range(1,4):
    # get spider obj
    r1 = requests.get(url, params={'page': page})

    r1.encoding = chardet.detect(r1.content)["encoding"]

    soup = BeautifulSoup(r1.text, 'html.parser')
    # 对第一页的高位玩家信息进行爬取
    # to high ranking-score players spider data
    if page == 1:
        '''
        spider in order
        rank
        sommoner's private website's url
        sommoner's id
        sommoner's rank
        sommoner's ranking-score
        sommoner's game level
        win march in rank
        lose march in rank
        '''

        for content in soup.find_all(name='ul', class_='ranking-highest__list'):
            for summoner in content.find_all(name='li'):
                for ranking in summoner.find_all(name='div', class_='ranking-highest__rank'):
                    # save number and alpha, isalnum is save number and alpha, isnumeric is save number
                    ranking_text = ''.join(list(filter(str.isalnum, ranking.text)))
                    print(ranking_text, end=' ')
                for id in summoner.find_all(name='a', class_='ranking-highest__name'):
                    print(id['href'], end=' ')
                    print(id.text, end=' ')
                for tier_info in summoner.find_all(name='div', class_='ranking-highest__tierrank'):
                    for tier in tier_info.find_all(name='span'):
                        tier_text=''.join(list(filter(str.isalnum, tier.text)))
                    for lp in tier_info.find_all(name='b'):
                        lp_text=''.join(list(filter(str.isalnum, lp.text)))
                    for level in content.find_all(name='div', class_='ranking-highest__level'):
                        level_text = ''.join(list(filter(str.isnumeric, level.text)))
                    print('{} {} {}'.format(tier_text, lp_text, level_text), end=' ')
                for win_lose in summoner.find_all(name='div', class_='winratio-graph'):
                    for win_times in win_lose.find_all(name='div', class_="winratio-graph__text winratio-graph__text--left"):
                        win_time_text = ''.join(list(filter(str.isalnum, win_times.text)))
                    for lose_times in win_lose.find_all(name='div', class_="winratio-graph__text winratio-graph__text--right"):
                        lose_time_text = ''.join(list(filter(str.isalnum, lose_times.text)))
                    print('{}:{}'.format(win_time_text, lose_time_text))
                # output txt file
                data_summoner_ranking_list += [{
                    'data_summoner_ranking_num': ranking_text,
                    'data_summoner_ranking_url': id['href'],
                    'data_summoner_ranking_name': id.text,
                    'data_summoner_ranking_tier': tier_text,
                    'data_summoner_ranking_lp': lp_text,
                    'data_summoner_ranking_level': level_text,
                    'data_summoner_ranking_win_times': win_time_text,
                    'data_summoner_ranking_lose_times': lose_time_text
                }]
                fobj.write("{}|{}|{}|{}|{}|{}|{}|{}\n".format(ranking_text, id['href'], id.text, tier_text, lp_text, level_text, win_time_text, lose_time_text))
    # spider player information
    for content in soup.find_all(name='table', class_='ranking-table'):
        '''
                spider in order
                rank
                sommoner's private website's url
                sommoner's id
                sommoner's rank
                sommoner's ranking-score
                sommoner's game level
                win march in rank
                lose march in rank
                '''
        for summoner in content.find_all(name='tr', class_='ranking-table__row'):
           for ranking in summoner.find_all(name='td', class_='ranking-table__cell ranking-table__cell--rank'):
               ranking_text=''.join(list(filter(str.isalnum, ranking.text)))
               print(ranking_text,end=' ')
           for id in summoner.find_all(name='td', class_='ranking-table__cell ranking-table__cell--summoner'):
               for id_url in id.find_all(name='a'):
                   print(id_url['href'], end=' ')
               for name in id.find_all(name='span'):
                   print(name.text, end=' ')
           for tier in summoner.find_all(name='td', class_='ranking-table__cell ranking-table__cell--tier'):
               tier_text=''.join(list(filter(str.isalnum, tier.text)))
               print(tier_text,end=' ')
           for lp in summoner.find_all(name='td', class_='ranking-table__cell ranking-table__cell--lp'):
               lp_text=''.join(list(filter(str.isalnum, lp.text)))
               print(lp_text,end=' ')
           for level in summoner.find_all(name='td', class_='ranking-table__cell ranking-table__cell--level'):
               level_text=''.join(list(filter(str.isalnum, level.text)))
               print(level_text, end=' ')
           for win_lose in summoner.find_all(name='div', class_='winratio-graph'):
               for win_times in win_lose.find_all(name='div', class_="winratio-graph__text winratio-graph__text--left"):
                   win_time_text=''.join(list(filter(str.isalnum, win_times.text)))
               for lose_times in win_lose.find_all(name='div', class_="winratio-graph__text winratio-graph__text--right"):
                   lose_time_text = ''.join(list(filter(str.isalnum, lose_times.text)))
               print('{}:{}'.format(win_time_text,lose_time_text))
           data_summoner_ranking_list += [{
                'data_summoner_ranking_num': ranking_text,
                'data_summoner_ranking_url': id_url['href'],
                'data_summoner_ranking_name': name.text,
                'data_summoner_ranking_tier': tier_text,
                'data_summoner_ranking_lp': lp_text,
                'data_summoner_ranking_level': level_text,
                'data_summoner_ranking_win_times': win_time_text,
                'data_summoner_ranking_lose_times': lose_time_text
            }]
           fobj.write("{}|{}|{}|{}|{}|{}|{}|{}\n".format(ranking_text, id_url['href'], name.text, tier_text, lp_text,
                                                         level_text, win_time_text, lose_time_text))
fobj.close()

# save json file by system version
system_version ='windows'
if system_version == 'linux':
    json_file_name = '/home/www/htdocs/wp-content/uploads/summoner_ranking.json'
    with open(json_file_name, 'w') as json_file_obj:
        json.dump(data_summoner_ranking_list, json_file_obj)
else:
    json_file_name = 'E:/data/summoner_ranking.json'
    with open(json_file_name, 'w') as json_file_obj:
        json.dump(data_summoner_ranking_list, json_file_obj)

# if summoner.find_all(name='td', class='ranking-table__cell ranking-table__cell--rank'):





