import requests
import chardet
from bs4 import BeautifulSoup

def get_info(input_url):
    url = input_url
    r1 = requests(url)


    return