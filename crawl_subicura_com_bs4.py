from bs4 import BeautifulSoup
import requests
import csv
import re
import io
from text_rank import *
from markdownify import markdownify as md


class Subicura:
    def __init__(self):
        self.req = requests.get('https://subicura.com')
        self.html = self.req.text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.file = open("../csv/subicura.csv", "w", encoding='utf-8', newline='')
        self.write = csv.writer(self.file)
        self.write.writerow(["title", "content", "url", "cnt", "date", "source"])

    def main(self):
        print("Subicura Crawl Start")
        main_url = "https://subicura.com"
        information = self.soup.find_all("a", {"itemprop": "url"})

        for target in information:
            sub_url = self.parse_url(str(target))
            title = self.parse_title(str(target))
            req = requests.get(main_url + sub_url)
            soup = BeautifulSoup(req.text, 'html.parser')
            date = soup.find("time")
            date = self.parse_date(date.contents[0])

            content_list = soup.find_all("p")
            text = ""
            f = io.open("text.txt", mode="w", encoding="utf-8")
            for each in content_list:
                text += each.get_text()
                f.writelines(each.get_text())
            f.close()
            self.extract_keyword()
            self.write.writerow([title, text[:200], main_url + sub_url, 0, date, "subicura"])
        self.file.close()
        print("Subicura Crawl End")

    def parse_title(self, title):
        title = title.split("itemprop=\"url\"")[1].lstrip(">").rstrip("</a>").lstrip().rstrip()
        if "span" in title:
            temp = title.split('<span class="series">')
            title = temp[0].rstrip()
            # title = temp[0].rstrip() + " " + temp[1].split('</span>')[0].rstrip()
        return title

    def parse_url(self, url):
        url = url.split("<a href=\"")[1].split("\" itemprop")[0]
        return url

    def parse_date(self, date):
        month_dic = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
        lst = date.split()
        date_string = lst[2] + "-" + month_dic[lst[1]] + "-" + lst[0]
        return date_string

    def extract_keyword(self):
        tr = TextRank(window=5, coefficient=1)
        print('Load...')
        stop_word = set([('있', 'VV'), ('하', 'VV'), ('되', 'VV'), ('없', 'VV')])
        tr.load(RawTaggerReader('text.txt'), lambda w: w not in stop_word and (w[1] in ('NNG', 'NNP')))
        print('Build...')
        tr.build()
        kw = tr.extract(0.1)
        for k in sorted(kw, key=kw.get, reverse=True):
            for each in k:
                print(each)
            # print("%s\t%g" % (k, kw[k]))


if __name__ == "__main__":
    s = Subicura()
    s.main()
