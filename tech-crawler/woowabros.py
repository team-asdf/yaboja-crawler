import requests
import csv
from bs4 import BeautifulSoup
import sys
sys.path.insert(0, '../keyword-module')
from get_keyword import getKeywords, githubTopicSearch

# TODO
# img 태그 검색

def getLinks():
    r = requests.get("http://woowabros.github.io/")
    source = r.text
    soup = BeautifulSoup(source, "lxml")

    link_list = []
    links = soup.find_all("div", {"class": "list-module"})
    for l in links:
        link = l.find("a")
        link_list.append("http://woowabros.github.io" + link['href'])

    return link_list


def getData(file, link):
    r = requests.get(link)
    content_source = r.text
    content_soup = BeautifulSoup(content_source, "lxml")

    title = content_soup.find("h1", {"class": "post-title"}).text.replace(u'\xa0',' ').replace('\t',' ')
    # keyword_list = getKeywords(title.lower())
    keyword_list = githubTopicSearch(title.lower())
    _keyword = ",".join(keyword_list)
    created_at = content_soup.find("time")['datetime'].split("T")[0]

    content = ""
    section_content = content_soup.find_all("div", {"class": "post-content"})
    for s in section_content:
        contents = s.find_all("p")
        for c in contents:
            content += c.text
    content = content.replace(u'\xa0',' ').replace('\t',' ').replace('<br>', ' ').replace("\n", ' ')
    source = "woowabros"
    file.writerow([title, content, link, source, _keyword, "NULL", created_at])


if __name__ == "__main__":
    link_list = getLinks()

    file = open("data/woowabros.csv", "w", encoding='utf-8', newline='')
    writefile = csv.writer(file)
    writefile.writerow(["title", "content", "url", "source", "keyword", "image", "createdAt"])
    for i in range(len(link_list)):
        getData(writefile, link_list[i])
    file.close()