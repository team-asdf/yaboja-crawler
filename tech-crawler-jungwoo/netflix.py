import requests
import csv
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from get_keyword import getKeywordsForMulti, getKeywords
import time


def getLinks():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    driver = webdriver.Chrome(os.path.dirname(os.path.realpath(__file__)) + "/chromedriver", chrome_options=options)
    driver.get("https://medium.com/netflix-techblog")
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
        f = open(os.path.dirname(os.path.realpath(__file__)) + "/data/netflix.csv", "r", encoding='utf-8')
        rdr = csv.reader(f)
        for line in rdr:
            already_list.append(line[2])
        f.close()
    except FileNotFoundError:
        f = open(os.path.dirname(os.path.realpath(__file__)) + "/data/netflix.csv", "w", encoding='utf-8', newline='')
        writefile = csv.writer(f)
        writefile.writerow(["title", "content", "url", "cnt", "source", "keyword", "image", "createdAt", "priority"])
        f.close()
    
    source = driver.page_source
    soup = BeautifulSoup(source, "lxml")
    driver.close()
    
    links_1 = soup.find_all("div", {"class": "col u-xs-marginBottom10 u-paddingLeft9 u-paddingRight12 u-paddingTop0 u-sm-paddingTop20 u-paddingBottom25 u-size4of12 u-xs-size12of12 u-marginBottom30"})
    links_2 = soup.find_all("div", {"class": "u-lineHeightBase postItem"})
    links_3 = soup.find_all("div", {"class": "col u-xs-marginBottom10 u-paddingLeft0 u-paddingRight0 u-marginBottom60"})

    for l in links_1:
        link = l.find("a")
        # print(link['href'])
        if link['href'] not in already_list:
            link_list.append(link['href'])

    for l in links_2:
        link = l.find("a")
        # print(link['href'])
        if link['href'] not in already_list:
            link_list.append(link['href'])

    for l in links_3:
        link = l.find("a")
        # print(link['href'])
        if link['href'] not in already_list:
            link_list.append(link['href'])

    return link_list


def getData(file, link, multi):
    r = requests.get(link)
    content_source = r.text
    content_soup = BeautifulSoup(content_source, "lxml")

    title = content_soup.select_one('div.section-content > div > h1').text.replace(u'\xa0',' ').replace('\t',' ').lstrip().rstrip().replace("\"", "").replace("\'", "")
    created_at = content_soup.find("time")['datetime'].split("T")[0]

    content = ""
    section_content = content_soup.find_all("div", {"class": "section-content"})
    for s in section_content:

        image = ""
        img = s.find("img")
        if img is not None:
            image = img['src']
        print(image)

        contents = s.find_all("p")
        for c in contents:
            content += c.text
    content = content.replace(u'\xa0',' ').replace('\t',' ').replace('<br>', ' ').replace("\n", ' ').lstrip().rstrip().replace("\"", "").replace("\'", "")
    source = "netflix"

    if multi:
        keyword_list = getKeywordsForMulti(title.lower(), content.lower(), source, False)
    else:
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


def main(multi):
    print("netflix")
    start = time.time()

    link_list = getLinks()

    file = open(os.path.dirname(os.path.realpath(__file__)) + "/data/netflix.csv", "a", encoding='utf-8', newline='')
    writefile = csv.writer(file)
    for i in range(len(link_list)):
        getData(writefile, link_list[i], multi)
    file.close()

    print(time.time() - start)


if __name__ == "__main__":
    main()