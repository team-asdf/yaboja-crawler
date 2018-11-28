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
    driver.get("https://slack.engineering/latest")
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
        f = open(os.path.dirname(os.path.realpath(__file__)) + "/data/slack.csv", "r", encoding='utf-8')
        rdr = csv.reader(f)
        for line in rdr:
            already_list.append(line[2])
        f.close()
    except FileNotFoundError:
        f = open(os.path.dirname(os.path.realpath(__file__)) + "/data/slack.csv", "w", encoding='utf-8', newline='')
        writefile = csv.writer(f)
        writefile.writerow(["title", "content", "url", "cnt", "source", "keyword", "image", "createdAt", "priority"])
        f.close()

    source = driver.page_source
    soup = BeautifulSoup(source, "lxml")
    driver.close()

    links = soup.find_all("div", {"class": "postArticle-readMore"})

    for l in links:
        link = l.find("a")
        if link['href'] not in already_list:
            link_list.append(link['href'])

    return link_list


def getData(file, link):
    r = requests.get(link)
    content_source = r.text
    content_soup = BeautifulSoup(content_source, "lxml")

    title = content_soup.select_one('div.section-content > div > h1').text.replace(u'\xa0',' ').replace('\t',' ')
    created_at = content_soup.find("time")['datetime'].split("T")[0]

    content = ""
    section_content = content_soup.find_all("div", {"class": "section-content"})
    for s in section_content:

        image = ""
        img = s.find("img")
        if img is not None:
            if img['src'].startswith("/"):
                image = "https://slack.engineering" + img['src']
            else:
                image = img['src']
        print(image)

        contents = s.find_all("p")
        for c in contents:
            content += c.text
    content = content.replace(u'\xa0',' ').replace('\t',' ').replace('<br>', ' ').replace("\n", ' ')
    source = "slack"

    # keyword_list = getKeywordsForMulti(title.lower(), content.lower(), source, False)
    keyword_list = getKeywords(title.lower(), content.lower(), source, False)
    if keyword_list:
        _keyword = ",".join(keyword_list)
    else:
        _keyword = ""

    file.writerow([title, content[:200] + "...", link, 0, source, _keyword, image, created_at, 0])

    updater = open(os.path.dirname(os.path.realpath(__file__)) + "/data/update.csv", "a", encoding='utf-8', newline='')
    update_writer = csv.writer(updater)
    update_writer.writerow([title, content[:200] + "...", link, 0, source, _keyword, image, created_at, 0])
    updater.close()


def main():
    print("slack")
    start = time.time()

    link_list = getLinks()

    file = open(os.path.dirname(os.path.realpath(__file__)) + "/data/slack.csv", "a", encoding='utf-8', newline='')
    writefile = csv.writer(file)
    for i in range(len(link_list)):
        try:
            getData(writefile, link_list[i])
        except:
            print("skip")
    file.close()

    print(time.time() - start)


if __name__ == "__main__":
    main()