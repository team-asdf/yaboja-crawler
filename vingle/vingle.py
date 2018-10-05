import requests
import os
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
import sys
sys.path.insert(0, '../keyword-module')
from get_keyword import getKeywords


def getLinks():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    driver = webdriver.Chrome(os.path.abspath("chromedriver.exe"), chrome_options=options)
    driver.get("https://medium.com/vingle-tech-blog/archive")
    driver.implicitly_wait(5)

    select_sorting = driver.find_element_by_xpath("//div[4]/button/span")
    select_sorting.click()
    driver.implicitly_wait(1)
    sort_by_latest = driver.find_element_by_xpath("//li[3]/button")
    sort_by_latest.click()

    # r = requests.get("https://medium.com/vingle-tech-blog/archive")
    # source = r.text
    source = driver.page_source
    soup = BeautifulSoup(source, "lxml")

    links = soup.find_all("div", {"class": "postArticle-readMore"})
    for l in links:
        link = l.find("a")
        link_list.append(link['href'])

    # print(link_list)
    return link_list


def getData(file, link):
    r = requests.get(link)
    content_source = r.text
    content_soup = BeautifulSoup(content_source, "lxml")

    title = content_soup.select_one('div.section-content > div > h1').text.replace(u'\xa0',' ').replace('\t',' ')
    print(title)

    keyword_list = getKeywords(title.lower())
    created_at = content_soup.find("time")['datetime'].split("T")[0]

    content = ""
    section_content = content_soup.find_all("div", {"class": "section-content"})
    for s in section_content:
        contents = s.find_all("p")
        for c in contents:
            content += c.text
            content += "\n\n"
    content = content.replace(u'\xa0',' ').replace('\t',' ').replace('<br>', ' ')

    # print(content)
    # result = dict(link=link, created_at=created_at, title=title, content=content)
    source = "medium"
    file.writerow([link, created_at, title, content, source])
    # return result


link_list = list()
link_list = getLinks()

file = open("data/vingle.csv", "w", encoding='utf-8', newline='')
writefile = csv.writer(file)
writefile.writerow(["url", "createdAt", "title", "content", "source"])
for i in range(len(link_list)):
    getData(writefile, link_list[i])
file.close()

    # with open(result['created_at'] + "-" + .replace("/", ",") + ".json", 'w') as outfile:
    #    json.dump(result, outfile)
    # output = json.dumps(result)