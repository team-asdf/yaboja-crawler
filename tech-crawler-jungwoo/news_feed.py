import feedparser
import re
import csv
from get_keyword import getKeywordsForMulti, getKeywords
import time
import os
import ssl


def clean_html(raw_html):
    """
    Utility function for replace HTML tags from string.
    """
    ltgt = re.compile('<.*?>')
    whitespace = re.compile('\s+')
        
    clean_text = whitespace.sub(" ", ltgt.sub("", raw_html)).replace("\n", " ")
    return clean_text


def feed_parsing(file, multi):
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context  # to solve SSLCertVerificationError problem

    link_list = ['https://www.computerworld.com/index.rss', 'https://www.recode.net/rss/index.xml']
    general_url = re.compile('(http(s)?:\/\/)([a-z0-9\w]+\.*)+[a-z0-9]{2,4}')

    for link in link_list:
        d = feedparser.parse(link)
        
        # print(source)
        for i in range(len(d.entries)):
            title = d['entries'][i]['title']
            content = clean_html(d['entries'][i]['description']).replace(u'\xa0',' ').replace('\t',' ').replace('<br>', ' ').replace("\n", ' ').lstrip().rstrip().replace("\"", "").replace("\'", "")
            link = d['entries'][i]['link']
            source = general_url.search(d['entries'][i]['link']).group().split('.')[1]
            
            if multi:
                keyword_list = getKeywordsForMulti(title.lower(), content.lower(), source, False)
            else:
                keyword_list = getKeywords(title.lower(), content.lower(), source, False)

            if keyword_list:
                _keyword = ",".join(keyword_list)
            else:
                _keyword = ""
            created_at = time.strftime("%Y-%m-%d", d['entries'][i].get("published_parsed", time.gmtime())).split("T")[0]
            
            file.writerow([title, content[:200] + "...", link, 0, source, _keyword, "", created_at, 0])

            updater = open(os.path.dirname(os.path.realpath(__file__)) + "/data/update.csv", "a", encoding='utf-8', newline='')
            update_writer = csv.writer(updater)
            update_writer.writerow([title, content[:200] + "...", link, 0, source, _keyword, "", created_at, 0])
            updater.close()


def main(multi):
    print("news_feed")
    file = open(os.path.dirname(os.path.realpath(__file__)) + "/data/news_feed.csv", "w", encoding='utf-8', newline='')
    writefile = csv.writer(file)
    writefile.writerow(["title", "content", "url", "cnt", "source", "keyword", "image", "createdAt", "priority"])
    feed_parsing(writefile, multi)
    file.close()


if __name__ == "__main__":
    main()