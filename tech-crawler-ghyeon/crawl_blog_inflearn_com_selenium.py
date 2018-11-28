from selenium import webdriver
import csv


class Inflearn:
    def __init__(self):
        # set webdriver options
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.options.add_argument('window-size=1920x1080')
        self.options.add_argument('disable-gpu')
        self.options.add_argument('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) '
                                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36')

        # webdriver path(Need to be Changed)
        self.driver = webdriver.Chrome('./webdriver/chromedriver', chrome_options=self.options)

        # csv
        self.file = open("./csv/inflearn.csv", "w", encoding='utf-8', newline='')
        self.write = csv.writer(self.file)
        self.write.writerow(["title", "content", "url", "cnt", "date", "source"])

    def crawl(self):
        print("Inflearn Crawl Start")
        # 인프런 블로그
        self.driver.get("http://blog.inflearn.com/category/develop/")
        page_idx = 1
        while 1:
            try:
                # to next page
                if page_idx != 1:
                    self.driver.find_element_by_css_selector('#main > nav > div > a.next.page-numbers').click()
                # Crawling
                for post_idx in range(2, 47):
                    self.driver.find_element_by_css_selector('#main > div:nth-child(' + str(post_idx) + ')').click()
                    title = self.driver.find_element_by_class_name('entry-header').text
                    url = self.driver.current_url
                    date = self.parse_date(self.driver.find_element_by_css_selector('time').text)
                    # print(date)
                    self.write.writerow([title, "temp", url, 0, date, "inflearn"])
                    # print("title:", self.driver.find_element_by_class_name('entry-header').text)
                    # print("url:", self.driver.current_url)
                    self.driver.back()
                page_idx += 1
            except:
                break
        print("Inflearn Crawl End")

    def main(self):
        self.crawl()
        self.file.close()
        self.driver.quit()

    def parse_date(self, date):
        date = date.split()
        for idx in range(len(date)):
            date[idx] = date[idx][:-1]
            # print(date[idx])
        date_string = date[0] + "-" + ("0" if len(date[1]) == 1 else "") + date[1] + "-" + date[2]
        return date_string


if __name__ == "__main__":
    instance = Inflearn()
    instance.main()

