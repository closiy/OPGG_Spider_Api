#!/usr/bin/python3
import requests
import chardet
import pymongo
import json
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
    champion_flag = {'data_champion_pos_url': data_champion_pos_url}  # flag of champion, to find out data

    '''
    get header info from OPGG champions page
    '''
    # header of pages, data-type as  position_role position_rate
    header = soup2.find(name='div', attrs=['class', 'l-champion-statistics-header'])
    li_position = header.find(name='li', class_= 'champion-stats-header__position champion-stats-header__position--active')

    # get and update information of rate
    rate_span = li_position.find(name='span', attrs=['class', 'champion-stats-header__position__rate'])
    champion_pos_rate = {'data_champion_pos_rate': rate_span.text}
    mycol.update_one(champion_flag, {'$set': {'data_champion_pos_rate': champion_pos_rate['data_champion_pos_rate']}})

    # get and update img of champion
    div_img = header.find(name='div', class_='champion-stats-header-info__image')
    champion_img = div_img.find(name='img')
    data_champion_img_url = 'https:' + champion_img.attrs['src']
    mycol.update_one(champion_flag, {'$set': {'data_champion_img_url': data_champion_img_url}})

    # get and update tier of champion
    div_tier = header.find(name='div', class_='champion-stats-header-info__tier')
    champion_tier = div_tier.find(name='b')
    data_champion_tier = champion_tier.text
    mycol.update_one(champion_flag, {'$set': {'data_champion_tier': data_champion_tier}})

    # get and update counter champion
    table_counter = header.find(name='table', class_='champion-stats-header-matchup__table champion-stats-header-matchup__table--strong tabItem')
    data_champion_counter_list = []
    i = 1
    for tr_counter in table_counter.find_all(name='tr'):
        data_champion_counter_url = 'https:' + tr_counter.find(name='img')['src']
        data_champion_counter_winrate = tr_counter.find(name='b').text
        data_champion_counter_id = get_champion_id_from_url(data_champion_counter_url)
        data_champion_counter_list += [{
            'data_champion_counter_id' + str(i): data_champion_counter_id,
            'data_champion_counter_url_' + str(i): data_champion_counter_url,
            'data_champion_counter_winrate_' + str(i): data_champion_counter_winrate}]
        i += 1
    mycol.update_one(champion_flag, {'$set': {'data_champion_counter_list': data_champion_counter_list}})

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
            'data_champion_anticounter_id' + str(i): data_champion_anticounter_id,
            'data_champion_anticounter_url_' + str(i): data_champion_anticounter_url,
            'data_champion_anticounter_winrate_' + str(i): data_champion_anticounter_winrate}]
        i += 1
    mycol.update_one(champion_flag, {'$set': {'data_champion_anticounter_list': data_champion_anticounter_list}})


    '''
    get main container of OPGG champion page
    request: main, item, skill, rune, trend, match up
    Overview of champion
    '''
    main_url = data_champion_pos_url + '#'
    r3 = requests.get(main_url)
    r3.encoding = chardet.detect(r3.content)["encoding"]
    soup3 = BeautifulSoup(r3.text, 'html.parser')
    main_contain = soup3.find(name='div', attrs=['class', 'tabItem Content championLayout-overview'])
    recommended_tbody_first = main_contain.find(name='tbody')
    i = 1
    data_spell_list = []
    '''
    get spell information of overview
    update spell id, url, win rate, match up to mongodb
    '''
    for tr_spells in recommended_tbody_first.find_all(name='tr'):
        j = 1
        for li_img in tr_spells.find_all(name='img'):
            # get summoner spells url and it's name
            if j == 1:
                data_spell_url_main = 'https:' + li_img.attrs['src']
                data_spell_id_main = get_champion_id_from_url(data_spell_url_main)
            else:
                data_spell_url_sub = 'https:' + li_img.attrs['src']
                data_spell_id_sub = get_champion_id_from_url(data_spell_url_sub)

            j += 1
        j = 1
        for strong_spells in tr_spells.find_all(name='strong'):
            # get match up rate and win rate
            if j == 1:
                data_spell_matchup = strong_spells.text
            else:
                data_spell_winrate = strong_spells.text
            j += 1

        data_spell_list += [{
            'data_spell_url_main_' + str(i): data_spell_url_main,
            'data_spell_id_main_' + str(i): data_spell_id_main,
            'data_spell_url_sub_' + str(i): data_spell_url_sub,
            'data_spell_id_sub_' + str(i): data_spell_id_sub,
            'data_spell_matchup_' + str(i): data_spell_matchup,
            'data_spell_winrate_' + str(i): data_spell_winrate
        }]
        i += 1
    mycol.update_one(champion_flag, {'$set': {'data_champion_anticounter_list': data_spell_list}})

    '''
    Recommended Skill Builds
    '''
    recommended_skill_builds = main_contain.find(name='table', class_='champion-skill-build__table')
    data_skill_list = ''
    for tr_skill in recommended_skill_builds.find_all(name='tr'):
        for th_skill in tr_skill.find_all(name='td'):
            for ch in th_skill.text:
                if ch.isupper():
                    data_skill_list += ch
    mycol.update_one(champion_flag, {'$set': {'data_champion_skill_list': data_skill_list}})

    '''
    Recommended Item Builds
    '''
    flag = 1
    for recommended_builds in main_contain.find_all(name='table', class_='champion-overview__table'):
        if flag == 2:
            recommended_item_builds = recommended_builds
        flag += 1
    data_item_list = []
    tbody_item = recommended_item_builds.find(name='tbody')
    flag = 0
    for tr_item in tbody_item.find_all(name='tr'):
        data_item_each_list = []
        if tr_item['class'] == ['champion-overview__row', 'champion-overview__row--first']:
            # get img of items
            for img_item in tr_item.find_all(name='img'):
                img_item_url = 'https:'+ img_item['src']
                if img_item_url.find('item') is not -1:
                    data_item_each_list += [{'item':img_item_url}]
            # get win rate and pick rate
            for strong_item in tr_item.find_all(name='strong'):
                data_item_each_list += [{'rate': strong_item.text}]
            flag += 1
        else:
            # get img of items
            for img_item in tr_item.find_all(name='img'):
                img_item_url = 'https:'+ img_item['src']
                if img_item_url.find('item') is not -1:
                    data_item_each_list += [{'item':img_item_url}]
            # get win rate and pick rate
            for strong_item in tr_item.find_all(name='strong'):
                data_item_each_list += [{'rate': strong_item.text}]
        if flag == 1:
            item_name ='init_item'
        if flag == 2:
            item_name = 'recommend_item'
        if flag == 3:
            item_name = 'shoes'

        data_item_list += [{item_name: data_item_each_list}]
    # data_item_list_json = json.dumps(data_item_list)    # change to json
    mycol.update_one(champion_flag, {'$set': {'data_champion_item_list': data_item_list}})


    '''
    Recommended Keystone rune Builds
    '''
    recommended_rune_1 = main_contain.find(name='tbody', class_='tabItem ChampionKeystoneRune-1')
    recommended_rune_2 = main_contain.find(name='tbody', class_='tabItem ChampionKeystoneRune-2')
    data_rune_list = []
    for tbody_rune in [recommended_rune_1, recommended_rune_2]:
        for tr_rune in tbody_rune.find_all(name='tr'):
            perk_rune_list_main = []
            perk_rune_list_sub = []
            fra_rune_list = []
            tmp_list = []

            # fragment img here
            fra_page = tr_rune.find(name='div', class_='fragment-page')
            for img_fra_url in fra_page.find_all(name='img'):
                if img_fra_url.attrs['class'] == ['active', 'tip']:
                    data_champion_rune_img_fra = 'https:' + img_fra_url['src']
                    tmp_list += [data_champion_rune_img_fra]

            fra_rune_list = [{'data_champion_rune_img_fra': tmp_list}]

            flag_p = 1
            tmp_list = []
            for perk_page in tr_rune.find_all(name='div', class_='perk-page'):
                data_champion_rune_img_main = 'https:'+ perk_page.find(name='img', class_='perk-page__image tip')['src']
                tmp_list += [data_champion_rune_img_main]
                # main and sub img here
                for div_rune_img in perk_page.find_all(name='div', class_=['perk-page__item  ', 'perk-page__item--active']):
                    data_champion_rune_img = 'https:' + div_rune_img.find(name='img')['src']
                    tmp_list += [data_champion_rune_img]

                if flag_p == 1:
                    perk_rune_list_main = [{'data_champion_rune_img_main': tmp_list}]
                elif flag_p == 2:
                    perk_rune_list_sub = [{'data_champion_rune_img_sub': tmp_list}]
                # elif flag_p ==3:
                #     data_rune_list += [{'data_champion_rune_img_fra': tmp_list}]
                flag_p += 1
            # rune stats of win and pick
            td_rune_stats = tr_rune.find(name='td', class_='champion-overview__stats champion-overview__stats--pick')
            flag = 1
            data_rune_rate_list = []
            for strong_rune_stats in td_rune_stats.find_all(name='strong'):
                if flag == 1:
                    data_champion_rune_pick = strong_rune_stats.text
                    data_rune_rate_list += [{'data_champion_rune_pick': data_champion_rune_pick}]
                    flag += 1
                elif flag == 2:
                    data_champion_rune_win = strong_rune_stats.text
                    data_rune_rate_list += [{'data_champion_rune_win': data_champion_rune_win}]
                    flag += 1
            data_rune_list += [{
                'main': perk_rune_list_main,
                'sub': perk_rune_list_sub,
                'fra': fra_rune_list,
                'rate': data_rune_rate_list
            }]
    # data_rune_list_json = json.dumps(data_rune_list)
    # print(data_rune_list)
    mycol.update_one(champion_flag, {'$set': {'data_champion_rune_list': data_rune_list}})

    '''
    get ranking and win rate of champions
    '''
    flag_t = 1
    champion_box_trend = main_contain.find(name='div', class_='champion-box champion-box--trend')
    for champion_box_trend in champion_box_trend.find_all(name='div', class_='champion-stats-trend'):
        champion_box_trend_ranking = champion_box_trend.find(name='div', class_='champion-stats-trend-rank')
        data_champion_trend_raning_num = champion_box_trend_ranking.find(name='b').text
        data_champion_trend_ranking_total = champion_box_trend_ranking.find(name='span').text.split('/')[1]
        data_champion_trend_ranking_rate = champion_box_trend.find(name='div',
                                                                        class_='champion-stats-trend-rate').text.replace(
            '\n',
            '').replace(
            '\t', '')
        data_champion_trend_ranking_content = champion_box_trend.find(name='div',
                                                                           class_='champion-stats-trend-average').text.replace(
            '\n', '').replace('\t', '')
        if flag_t == 1:
            data_trend_list_win = [{
                'ranking_no': data_champion_trend_raning_num,
                'ranking_total': data_champion_trend_ranking_total,
                'ranking_rate': data_champion_trend_ranking_rate,
                'ranking_content': data_champion_trend_ranking_content
            }]
            flag_t += 1
        elif flag_t == 2:
            data_trend_list_pick = [{
                'ranking_no': data_champion_trend_raning_num,
                'ranking_total': data_champion_trend_ranking_total,
                'ranking_rate': data_champion_trend_ranking_rate,
                'ranking_content': data_champion_trend_ranking_content
            }]
            break
    # print(data_trend_list_pick)
    # print(data_trend_list_win)
    mycol.update_one(champion_flag, {'$set': {'data_champion_win_stats': data_trend_list_win}})
    mycol.update_one(champion_flag, {'$set': {'data_champion_pick_stats': data_trend_list_pick}})
    # output data

    # print(mycol.find_one(champion_flag))




if __name__ == '__main__':
    # connect to mongodb
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['demacia_db']
    mycol = mydb['champions']

    # test data of 'neeko'
    data_champion_key = 'aatrox'
    data_champion_pos_url = 'https://www.op.gg/champion/ekko/statistics/mid'
    get_champions_data(data_champion_pos_url, data_champion_key, mycol)