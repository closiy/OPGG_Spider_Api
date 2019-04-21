import requests
from bs4 import BeautifulSoup
import chardet

def getImgFromTmail(url):
    r1 = requests.get(url)
    r1.encoding = chardet.detect(r1.content)["encoding"]
    soup = BeautifulSoup(r1.text, 'html.parser')
    print(soup)

if __name__ == '__main__':
    url = 'https://nike.tmall.com/i/asynSearch.htm?_ksTS=1555658737054_118&callback=jsonp119&mid=w-14234872789-0&wid=14234872789&path=/category-1394899094.htm&spm=a1z10.5-b-s.w4011-14234872789.358.2dce295bu0ZJj5&catId=1394899094&pageNo=3&scid=1394899094'
    getImgFromTmail(url)