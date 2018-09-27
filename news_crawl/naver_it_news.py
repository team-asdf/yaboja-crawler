from selenium import webdriver
from bs4 import BeautifulSoup
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# set webdriver options
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('disable-gpu')
options.add_argument('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36')

# webdriver path
driver = webdriver.Chrome('/Users/ghyeon/Documents/chromedriver/chromedriver', chrome_options=options)

# Naver IT/Science news
driver.get("https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=105")

# driver.implicitly_wait(1)

dic = dict()

# 각 섹션별 1 ~ 10페이지의 뉴스 크롤
for i in range(1, 9):
    section = driver.find_element_by_css_selector('#snb > ul > li:nth-child(' + str(i) + ')').text
    dic[section] = dict()
    print(section, "crawl start")
    driver.find_element_by_css_selector('#snb > ul > li:nth-child(' + str(i) + ')').click()
    paging_list = driver.find_element_by_css_selector('#main_content > div.paging').text.split()
    article_num = 1
    for page_num in paging_list:
        if page_num != '1':
            if len(paging_list) == 2:
                driver.find_element_by_css_selector('#main_content > div.paging > a').click()
            else:
                if page_num != '1' and page_num != '다음':
                    driver.find_element_by_css_selector(
                        '#main_content > div.paging > a:nth-child(' + page_num + ')').click()
        for j in range(1, 11):
            try:
                dic[section][article_num] = dict()
                driver.find_element_by_css_selector(
                    '#main_content > div.list_body.newsflash_body > ul.type06_headline > li:nth-child(' +
                    str(j) + ') > dl > dt:nth-child(2) > a').click()
                dic[section][article_num]['title'] = driver.find_element_by_css_selector('#articleTitle').text
                # dic[section][article_num]['text'] = driver.find_element_by_css_selector('#articleBodyContents').text
                print(dic[section][article_num]['title'])
                article_num += 1
                driver.back()
            except:
                try:
                    dic[section][article_num] = dict()
                    driver.find_element_by_css_selector(
                        '#main_content > div.list_body.newsflash_body > ul.type06_headline > li:nth-child(' +
                        str(j) + ') > dl > dt > a').click()
                    dic[section][article_num]['title'] = driver.find_element_by_css_selector('#articleTitle').text
                    # dic[section][article_num]['text'] = driver.find_element_by_css_selector('#articleBodyContents').text
                    print(dic[section][article_num]['title'])
                    article_num += 1
                    driver.back()
                except:
                    print("fail")
                    driver.back()
                    pass
        for j in range(1, 11):
            try:
                dic[section][article_num] = dict()
                driver.find_element_by_css_selector(
                    '#main_content > div.list_body.newsflash_body > ul.type06 > li:nth-child(' +
                    str(j) + ') > dl > dt:nth-child(2) > a').click()
                dic[section][article_num]['title'] = driver.find_element_by_css_selector('#articleTitle').text
                # dic[section][article_num]['text'] = driver.find_element_by_css_selector('#articleBodyContents').text
                print(dic[section][article_num]['title'])
                article_num += 1
                driver.back()
            except:
                try:
                    dic[section][article_num] = dict()
                    driver.find_element_by_css_selector(
                        '#main_content > div.list_body.newsflash_body > ul.type06 > li:nth-child(' +
                        str(j) + ') > dl > dt > a').click()
                    dic[section][article_num]['title'] = driver.find_element_by_css_selector('#articleTitle').text
                    # dic[section][article_num]['text'] = driver.find_element_by_css_selector('#articleBodyContents').text
                    print(dic[section][article_num]['title'])
                    article_num += 1
                    driver.back()
                except:
                    print("fail")
                    driver.back()
                    pass
    print(section, "crawl complete\n")
    driver.back()

driver.quit()

with open(os.path.join(BASE_DIR, 'result.json'), 'w+') as json_file:
    json.dump(dic, json_file)
