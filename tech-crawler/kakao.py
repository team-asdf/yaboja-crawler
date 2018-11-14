import requests
import csv
from bs4 import BeautifulSoup
from get_keyword import getKeywordsForMulti
import time


def getLinks():
    i = 1
    link_list = []
    already_list = []

    try:
        f = open("data/kakao.csv", "r", encoding='utf-8')
        rdr = csv.reader(f)
        for line in rdr:
            already_list.append(line[2])
    except FileNotFoundError:
        pass

    while True:
        if i == 1:
            r = requests.get("http://tech.kakao.com/")
        else:
            r = requests.get("http://tech.kakao.com/page/" + str(i))
        
        source = r.text
        soup = BeautifulSoup(source, "lxml")

        links = soup.find_all("li", {"class": "post-item post "})
        if not links:
            break

        for l in links:
            link = l.find("a")
            if "http://tech.kakao.com" + link['href'] not in already_list:
                link_list.append("http://tech.kakao.com" + link['href'])

        i += 1

    return link_list


def getData(file, link):
    r = requests.get(link)
    content_source = r.text
    content_soup = BeautifulSoup(content_source, "lxml")

    title = content_soup.select_one('div#cover > div > h1').text.replace(u'\xa0',' ').replace('\t',' ')    
    created_at = content_soup.select_one('p#post-date').text[0:10]

    content = ""
    section_content = content_soup.find_all("div", {"id": "post-content"})
    for s in section_content:
        contents = s.find_all("p")
        for c in contents:
            content += c.text
    content = content.replace(u'\xa0',' ').replace('\t',' ').replace('<br>', ' ').replace("\n", ' ')
    source = "kakao"

    keyword_list = getKeywordsForMulti(title.lower(), content.lower(), source)
    if keyword_list:
        _keyword = ",".join(keyword_list)
    else:
        _keyword = ""    

    file.writerow([title, content, link, 0, source, _keyword, "NULL", created_at])


def main():
    print("kakao")
    start = time.time()

    link_list = getLinks()

    file = open("data/kakao.csv", "w", encoding='utf-8', newline='')
    writefile = csv.writer(file)
    writefile.writerow(["title", "content", "url", "cnt", "source", "keyword", "image", "createdAt"])
    for i in range(len(link_list)):
        getData(writefile, link_list[i])
    file.close()

    print(time.time() - start)


if __name__ == "__main__":
    main()