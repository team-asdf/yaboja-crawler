import os
import csv

from dev_blog_crawl.crawl_blog_inflearn_com_selenium import Inflearn
from dev_blog_crawl.crawl_oracloud_kr import Oracle
from dev_blog_crawl.crawl_subicura_com_bs4 import Subicura


crawl_list = [Inflearn(), Oracle(), Subicura()]


def merge_files():
    csv_list = []
    for file in os.listdir("./csv"):
        if file.endswith(".csv"):
            if file != "main.csv":
                csv_list.append(file)

    temp_lst = list()
    temp_lst.append(["title", "content", "url", "cnt", "date", "source"])
    for file in csv_list:
        raw = open("./csv/" + file, "r", encoding="utf-8")
        lst = list(csv.reader(raw))
        for idx in range(1, len(lst)):
            temp_lst.append(lst[idx])
        raw.close()

    write = open("./csv/main.csv", "w", encoding="utf-8")
    writer = csv.writer(write)

    for each in temp_lst:
        writer.writerow(each)

    write.close()


def crawl(target):
    target.main()


def main():
    print("Full Operation Start")
    for each in crawl_list:
        crawl(each)
    print("Full Operation End")


if __name__ == "__main__":
    main()
    merge_files()