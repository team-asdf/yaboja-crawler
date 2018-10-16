import feedparser
import re
import csv
import sys
sys.path.insert(0, '../keyword-module')
from get_keyword import getKeywords
import time


def clean_html(raw_html):
    """
    Utility function for replace HTML tags from string.
    """
    ltgt = re.compile('<.*?>')
    whitespace = re.compile('\s+')
        
    clean_text = whitespace.sub(" ", ltgt.sub("", raw_html)).replace("\n", " ")
    return clean_text


def feed_parsing(file):
    link_list = ['https://www.computerworld.com/index.rss', 'https://www.recode.net/rss/index.xml']
    general_url = re.compile('(http(s)?:\/\/)([a-z0-9\w]+\.*)+[a-z0-9]{2,4}')

    for link in link_list:
        d = feedparser.parse(link)
        
        # print(source)

        for i in range(len(d.entries)):
            title = d['entries'][i]['title']
            content = clean_html(d['entries'][i]['description'])
            link = d['entries'][i]['link']
            source = general_url.search(d['entries'][i]['link']).group().split('.')[1]
            keyword_list = getKeywords(title.lower())
            _keyword = ",".join(keyword_list)
            created_at = time.strftime("%Y-%m-%dT%H:%M:%S", d['entries'][i].get("published_parsed", time.gmtime())).split("T")[0]
            
            file.writerow([title, content, link, source, "_keyword", "NULL", created_at])


if __name__ == "__main__":
    file = open("data/news_feed.csv", "w", encoding='utf-8', newline='')
    writefile = csv.writer(file)
    writefile.writerow(["title", "content", "url", "source", "keyword", "image", "createdAt"])
    feed_parsing(writefile)
    file.close()