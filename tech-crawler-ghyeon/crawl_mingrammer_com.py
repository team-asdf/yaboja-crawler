from bs4 import BeautifulSoup
import requests
import csv
import io
from text_rank import *
import json
import re


class Mingrammer:
    def __init__(self):
        self.file = open("./csv/mingrammer.csv", "w", encoding='utf-8', newline='')
        self.write = csv.writer(self.file)
        self.write.writerow(["title", "content", "url", "cnt", "source", "keyword", "image", "createdAt", "priority"])
        self.main_url = "https://mingrammer.com"
        json_file = open("keywords.json", encoding="utf-8")
        self.keyword_dict = json.load(json_file)
        json_file.close()

    def crawl(self):
        try:
            main_file = open("./csv/main.csv", 'r', encoding="utf-8")
        except FileNotFoundError:
            main_list = []
        else:
            main_list = list(csv.reader(main_file))
            main_file.close()
        for i in range(1, 5):
            if i == 1:
                page_url = self.main_url
            else:
                page_url = self.main_url + "/page/" + str(i)
            req = requests.get(page_url)
            soup = BeautifulSoup(req.text, 'html.parser')
            tag_lst = list(soup.find_all('li'))
            url_lst = []
            for each in tag_lst:
                to_crawl = self.parse_url(str(each))
                url_lst.append(to_crawl)
            for url in url_lst:
                temp_req = requests.get(url)
                temp_soup = BeautifulSoup(temp_req.text, 'html.parser')
                title = str(temp_soup.find('h1').text).lstrip().rstrip().replace("\n", " ").replace("\"", "").replace("\'", "")
                content = ""
                for each in temp_soup.find_all('p'):
                    content += each.text.lstrip().rstrip().replace("\n", " ").replace("\"", "").replace("\'", "")

                cnt = 0
                source = "mingrammer"
                keyword_list = sorted(list(set(self.extract_keyword(content))))
                keyword = ""
                for idx in range(len(keyword_list)):
                    keyword += keyword_list[idx]
                    if idx != len(keyword_list) - 1:
                        keyword += ","
                if keyword == "":
                    keyword = "etc"
                if temp_soup.find("img") is None:
                    image = "https://mingrammer.com/images/avatar.png"
                else:
                    image = str(temp_soup.find("img"))
                    if ".." in image:
                        image = self.main_url + image.split("src=\"..")[1].split("\"/>")[0]
                    else:
                        if "http" not in image:
                            image = self.main_url + image.split("src=\"")[1].split("\"/>")[0]
                        else:
                            image = image.split("src=\"")[1].split("\"/>")[0]

                priority = 0
                createdAt = self.parse_date(str(temp_soup.find("h2", {"class": "headline"}).text).split()[:3])
                write_data = [title, content[:199] + "...", url, cnt, source, keyword, image, createdAt, priority]
                if write_data in main_list:
                    break
                self.write.writerow(write_data)
        self.file.close()

    def extract_keyword(self, text):
        f = open("text.txt", 'w', encoding="utf-8")
        f.write(text)
        f.close()
        tr = TextRank(window=5, coefficient=1)
        print('Load...')
        stop_word = set([('있', 'VV'), ('하', 'VV'), ('되', 'VV'), ('없', 'VV')])
        tr.load(RawTaggerReader('text.txt'), lambda w: w not in stop_word and (w[1] in ('NNG', 'NNP')))
        print('Build...')
        tr.build()
        kw = tr.extract(0.1)
        keyword_lst = []
        for k in sorted(kw, key=kw.get, reverse=True):
            for each in k:
                temp_keyword = self.check_keyword(each[0])
                if temp_keyword != "etc" and temp_keyword != "":
                    keyword_lst.append(temp_keyword)
                    # keyword = temp_keyword
                    # return temp_keyword
        return keyword_lst

    def check_keyword(self, keyword):
        for each in self.keyword_dict:
            if keyword in self.keyword_dict[each]:
                return each
        return "etc"

    def parse_url(self, data):
        data = data.split("href=\"")[1].split("\">")[0]
        return data

    def parse_date(self, data):
        month_dic = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07",
                     "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
        return_data = ""
        data[1] = data[1][:-1]
        if len(data[1]) == 1:
            data[1] = "0" + data[1]
        return_data += data[2] + "-" + month_dic[data[0]] + "-" + data[1]
        # print(return_data)
        return return_data

    def main(self):
        print("mingrammer Crawl Start")
        self.crawl()
        print("mingrammer Crawl End")


if __name__ == "__main__":
    s = Mingrammer()
    s.main()
