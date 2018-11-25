import requests
import csv
from bs4 import BeautifulSoup
from get_keyword import getKeywordsForMulti
import time
import os
from selenium import webdriver
import datetime


def getLinks():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    driver = webdriver.Chrome(os.path.dirname(os.path.realpath(__file__)) + "/chromedriver", chrome_options=options)
    driver.get("https://blog.openai.com/")
    driver.implicitly_wait(7)

    SCROLL_PAUSE_TIME = 3

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    link_list = []
    already_list = []

    try:
        f = open(os.path.dirname(os.path.realpath(__file__)) + "/data/openai.csv", "r", encoding='utf-8')
        rdr = csv.reader(f)
        for line in rdr:
            already_list.append(line[2])
        f.close()
    except FileNotFoundError:
        f = open(os.path.dirname(os.path.realpath(__file__)) + "/data/openai.csv", "w", encoding='utf-8', newline='')
        writefile = csv.writer(f)
        writefile.writerow(["title", "content", "url", "cnt", "source", "keyword", "image", "createdAt", "priority"])
        f.close()

    source = driver.page_source
    soup = BeautifulSoup(source, "lxml")
    driver.close()
    
    links = soup.find_all("article", {"class": "Shared-Card"})

    for l in links:
        link = l.find("a")
        if "https://blog.openai.com" + link['href'] not in already_list:
            link_list.append("https://blog.openai.com" + link['href'])
            print("https://blog.openai.com" + link['href'])

    return link_list


def getData(file, link):
    r = requests.get(link)
    content_source = r.text
    content_soup = BeautifulSoup(content_source, "lxml")

    title = content_soup.find('h1', {"class": "PostHeader-title"}).text.replace(u'\xa0',' ').replace('\t',' ')
    created_at = content_soup.find("meta", property="article:published_time")['content'].split("T")[0]
    print(created_at)

    content = ""
    section_content = content_soup.find_all("section", {"class": "post-content"})
    for s in section_content:
        contents = s.find_all("p")
        for c in contents:
            content += c.text
    content = content.replace(u'\xa0',' ').replace('\t',' ').replace('<br>', ' ').replace("\n", ' ')
    source = "openai"

    keyword_list = getKeywordsForMulti(title.lower(), content.lower(), source)
    if keyword_list:
        _keyword = ",".join(keyword_list)
    else:
        _keyword = ""

    file.writerow([title, content, link, 0, source, _keyword, "NULL", created_at, 0])


def main():
    print("openai")
    start = time.time()

    link_list = getLinks()

    file = open(os.path.dirname(os.path.realpath(__file__)) + "/data/openai.csv", "a", encoding='utf-8', newline='')
    writefile = csv.writer(file)
    for i in range(len(link_list)):
        getData(writefile, link_list[i])
    file.close()

    print(time.time() - start)


if __name__ == "__main__":
    main()