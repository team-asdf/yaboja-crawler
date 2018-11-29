from bs4 import BeautifulSoup
import requests
import csv
from text_rank import *
import json


class Tae:
    def __init__(self):
        self.file = open("./csv/taetaetae.csv", "w", encoding='utf-8', newline='')
        self.write = csv.writer(self.file)
        self.write.writerow(["title", "content", "url", "cnt", "source", "keyword", "image", "createdAt", "priority"])
        self.main_url = "https://taetaetae.github.io"
        json_file = open("keywords.json", encoding="utf-8")
        self.keyword_dict = json.load(json_file)
        json_file.close()

    def main(self):
        self.crawl()

    def crawl(self):
        page_idx = 1
        while 1:
            if page_idx == 1:
                url = self.main_url
            else:
                url = self.main_url + "/page/" + str(page_idx)

            req = requests.get(url)
            soup = BeautifulSoup(req.text, 'html.parser')
            sub_url_tag_list = soup.find_all("a", {"class": "link-unstyled"})
            if sub_url_tag_list == []:
                break
            sub_url_list = []
            for each in sub_url_tag_list:
                sub_url_list.append(self.parse_sub_url(str(each)))
            for sub_url in sub_url_list:
                temp_url = self.main_url + sub_url
                temp_req = requests.get(temp_url)
                temp_soup = BeautifulSoup(temp_req.text, "html.parser")
                title = temp_soup.find("h1", {"class": "post-title"}).text.lstrip().rstrip().replace("\"", "").replace("\'", "")
                content = ""
                content_tag_list = temp_soup.find_all("p")
                for content_idx in range(1, len(content_tag_list)):
                    content += content_tag_list[content_idx].text.lstrip().rstrip().replace("\n", " ").replace("\"", "").replace("\'", "")
                # print(content)
                keyword_list = self.extract_keyword(content)
                keyword = ""
                for idx in range(len(keyword_list)):
                    keyword += keyword_list[idx]
                    if idx != len(keyword_list) - 1:
                        keyword += ","
                if keyword == "":
                    keyword = "etc"
                image_tag_list = temp_soup.find_all("img", {"class": "fig-img"})
                if len(image_tag_list) == 0:
                    image = self.main_url + "/assets/images/profile.png"
                else:
                    image = self.main_url + self.parse_image_url(str(image_tag_list[0]))
                source = "taetaetae"
                cnt = 0
                createdAt = self.parse_date(temp_soup.find("time").text.lstrip().rstrip())
                # print(createdAt)
                priority = 0
                write_data = [title, content[:199] + "...", temp_url, cnt, source, keyword, image, createdAt, priority]
                self.write.writerow(write_data)
            page_idx += 1
        self.file.close()

    def parse_sub_url(self, data):
        data = data.split("href=\"")[1].split("\">")[0]
        return data

    def parse_image_url(self, data):
        data = data.split("src=\"")[1].split("\"/>")[0]
        return data

    def parse_date(self, data):
        data = data.split()
        month_dic = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07",
                     "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
        return_data = ""
        data[1] = data[1][:-1]
        if len(data[1]) == 1:
            data[1] = "0" + data[1]
        return_data += data[2] + "-" + month_dic[data[0]] + "-" + data[1]
        # print(return_data)
        return return_data

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


if __name__ == "__main__":
    s = Tae()
    s.crawl()
