import requests
import csv
from bs4 import BeautifulSoup
from get_keyword import getKeywordsForMulti
import time


def getLinks():
    link_list = []
    already_list = []

    try:
        f = open("data/woowabros.csv", "r", encoding='utf-8')
        rdr = csv.reader(f)
        for line in rdr:
            already_list.append(line[2])
        f.close()
    except FileNotFoundError:
        f = open("data/woowabros.csv", "w", encoding='utf-8', newline='')
        writefile = csv.writer(f)
        writefile.writerow(["title", "content", "url", "cnt", "source", "keyword", "image", "createdAt"])
        f.close()
            
    r = requests.get("http://woowabros.github.io/")
    source = r.text
    soup = BeautifulSoup(source, "lxml")
    links = soup.find_all("div", {"class": "list-module"})

    for l in links:
        link = l.find("a")
        if "http://woowabros.github.io" + link['href'] not in already_list:
            link_list.append("http://woowabros.github.io" + link['href'])

    return link_list


def getData(file, link):
    r = requests.get(link)
    content_source = r.text
    content_soup = BeautifulSoup(content_source, "lxml")

    title = content_soup.find("h1", {"class": "post-title"}).text.replace(u'\xa0',' ').replace('\t',' ')    
    created_at = content_soup.find("time")['datetime'].split("T")[0]

    content = ""
    section_content = content_soup.find_all("div", {"class": "post-content"})
    for s in section_content:
        contents = s.find_all("p")
        for c in contents:
            content += c.text
    content = content.replace(u'\xa0',' ').replace('\t',' ').replace('<br>', ' ').replace("\n", ' ')
    source = "woowabros"

    keyword_list = getKeywordsForMulti(title.lower(), content.lower(), source)
    if keyword_list:
        _keyword = ",".join(keyword_list)
    else:
        _keyword = ""

    file.writerow([title, content, link, 0, source, _keyword, "NULL", created_at])


def main():
    print("woowabros")
    start = time.time()

    link_list = getLinks()

    file = open("data/woowabros.csv", "a", encoding='utf-8', newline='')
    writefile = csv.writer(file)
    for i in range(len(link_list)):
        getData(writefile, link_list[i])
    file.close()

    print(time.time() - start)


if __name__ == "__main__":
    main()