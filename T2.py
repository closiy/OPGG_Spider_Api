from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(executable_path=(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'), chrome_options=chrome_options)
driver.get("https://nike.tmall.com/i/asynSearch.htm?_ksTS=1555658737054_118&callback=jsonp119&mid=w-14234872789-0&wid=14234872789&path=/category-1394899094.htm&spm=a1z10.5-b-s.w4011-14234872789.358.2dce295bu0ZJj5&catId=1394899094&pageNo=3&scid=1394899094")
print(driver)
data = driver.find_elements_by_tag_name('img')
print(data)
for img_url in data:
    print(img_url.get_attribute('src'))
