from bs4 import BeautifulSoup
import requests
import csv


class Oracle:
    def __init__(self):
        self.file = open("../csv/oracle.csv", "w", encoding='utf-8', newline='')
        self.write = csv.writer(self.file)
        self.write.writerow(["title", "content", "url", "cnt", "date", "source"])

    def main(self):
        print("Oracle Crawl Start")
        idx = 1
        while 1:
            if idx == 1:
                page = 'http://www.oracloud.kr'
            else:
                page = 'http://www.oracloud.kr/page/' + str(idx) + '/'
            req = requests.get(page)
            html = req.text
            if '<h1>404</h1>' in html:
                break
            soup = BeautifulSoup(html, 'html.parser')
            links = list(soup.find_all('a', {"rel": "bookmark"}))
            for each in links:
                title = self.parse_title(str(each))
                url = self.parse_url(str(each))
                temp_html = requests.get(url).text
                time = temp_html.split("datetime=\"")[1][:10]
                # print(time)
                self.write.writerow([title, "temp", url, 0, time, "oracloud"])

            idx += 1
        print("Oracle Crawl End")

    def parse_url(self, url):
        url = url.split("=\"")[1].split("\" rel")[0]
        return url

    def parse_title(self, title):
        title = title.split("bookmark\">")[1].split("</a>")[0]
        return title


if __name__ == "__main__":
    s = Oracle()
    s.main()