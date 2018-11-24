from bs4 import BeautifulSoup
import requests
import csv
import io
from text_rank import *
import json
import re


class Luavis:
    def __init__(self):
        self.file = open("./csv/luavis.csv", "w", encoding='utf-8', newline='')
        self.write = csv.writer(self.file)
        self.write.writerow(["title", "content", "url", "cnt", "source", "keyword", "image", "createdAt"])
        self.main_url = "https://b.luavis.kr"
        json_file = open("keywords.json", encoding="utf-8")
        self.keyword_dict = json.load(json_file)
        json_file.close()

    def crawl(self):
        req = requests.get("https://b.luavis.kr/")
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        tag_lst = soup.find_all("h2")
        url_lst = []
        for each in tag_lst:
            temp_sub = str(each).split()[3].split("\">")[0].split("href=\"")[1]
            url_lst.append(temp_sub)
        for sub_url in url_lst:
            temp_req = requests.get(self.main_url + sub_url)
            temp_html = temp_req.text
            temp_soup = BeautifulSoup(temp_html, 'html.parser')
            title = self.parse_title(str(temp_soup.find("h1", {"class": "post-title"})))
            content_list = list(temp_soup.find_all("p"))
            content = ""
            for each in content_list[3:]:
                content += each.get_text()
            url = self.main_url + sub_url
            cnt = 0
            source = "Luavis' Dev Story"
            keyword_list = list(set(self.extract_keyword(content)))
            keyword = ""
            for idx in range(len(keyword_list)):
                keyword += keyword_list[idx]
                if idx != len(keyword_list) - 1:
                    keyword += ","
            if keyword == "":
                keyword = "etc"
            image = self.main_url + str(temp_soup.find("img")).split("src=\"")[1].split("\"/>")[0]
            print(image)
            createdAt = self.parse_date(str(temp_soup.find("p", {"class": "post-meta"})))
            self.write.writerow([title, content[:200], url, cnt, source, keyword, image, createdAt])
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

    def main(self):
        print("Luavis Crawl Start")
        self.crawl()
        print("Luavis Crawl End")

    def parse_title(self, data):
        data = data.split(">")[2].split("</a")[0]
        return data

    def parse_date(self, data):
        month_dic = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07",
                     "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
        return_data = ""
        data = data.split("\">")[1].split("</p>")[0]
        data = data.split()
        data[1] = data[1][:-1]
        return_data += data[2] + "-" + month_dic[data[0]] + "-" + data[1]
        # print(return_data)
        return return_data


if __name__ == "__main__":
    s = Luavis()
    s.main()