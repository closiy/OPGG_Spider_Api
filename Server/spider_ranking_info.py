import requests
import chardet
from bs4 import BeautifulSoup

fobj = open('ranking.txt', 'w')#文件写入

url = 'http://www.op.gg/ranking/ladder/'

'''
根据页数爬取玩家的数据
range(1,n) n为要爬取的页数
'''
for page in range(1,4):
    #获取爬取对象
    r1 = requests.get(url, params={'page': page})
    r1.encoding = chardet.detect(r1.content)["encoding"]
    soup = BeautifulSoup(r1.text, 'html.parser')
    #对第一页的高位玩家信息进行爬取
    if page == 1:
        '''
        依次爬取
        排名
        玩家个人信息的url
        玩家的id
        玩家段位
        玩家段位分
        玩家游戏等级
        玩家排位赢场数
        玩家排位输场数
        '''
        for content in soup.find_all(name='ul', class_='ranking-highest__list'):
            for summoner in content.find_all(name='li'):
                for ranking in summoner.find_all(name='div', class_='ranking-highest__rank'):
                    #对文本进行仅保留数字和字母 isalnum 是保留数字和字母 isnumeric 是仅保留数字
                    ranking_text=''.join(list(filter(str.isalnum, ranking.text)))
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
                #输出到txt文件
                fobj.write("{}|{}|{}|{}|{}|{}|{}|{}\n".format(ranking_text, id['href'], id.text, tier_text, lp_text, level_text, win_time_text, lose_time_text))
    #对普通玩家信息爬取
    for content in soup.find_all(name='table', class_='ranking-table'):
        '''
                依次爬取
                排名
                玩家个人信息的url
                玩家的id
                玩家段位
                玩家段位分
                玩家游戏等级
                玩家排位赢场数
                玩家排位输场数
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

           fobj.write("{}|{}|{}|{}|{}|{}|{}|{}\n".format(ranking_text, id_url['href'], name.text, tier_text, lp_text, level_text, win_time_text, lose_time_text))



fobj.close()

# if summoner.find_all(name='td', class='ranking-table__cell ranking-table__cell--rank'):





