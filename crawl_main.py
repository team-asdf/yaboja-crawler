import os
import csv
import time

from crawl_luavis_kr import Luavis
from crawl_subicura_com import Subicura
from crawl_mingrammer_com import Mingrammer


crawl_list = [Luavis(), Subicura(), Mingrammer()]


def merge_files():
    csv_list = []
    for file in os.listdir("./csv"):
        if file.endswith(".csv"):
            if file != "main.csv":
                csv_list.append(file)

    temp_lst = list()
    temp_lst.append(["title", "content", "url", "cnt", "source", "keyword", "image", "createdAt"])
    for file in csv_list:
        raw = open("./csv/" + file, "r", encoding="utf-8")
        lst = list(csv.reader(raw))
        for idx in range(1, len(lst)):
            temp_lst.append(lst[idx])
        raw.close()

    write = open("./csv/main.csv", "w", encoding="utf-8")
    writer = csv.writer(write)

    for each in temp_lst:
        each = each.replace("\"", "")
        writer.writerow(each)

    write.close()


def crawl(target):
    target.main()


def main():
    start = time.time()
    print("Full Operation Start")
    for each in crawl_list:
        crawl(each)
    merge_files()
    print("Full Operation End")
    print("Time Elapsed:", int(time.time() - start))


if __name__ == "__main__":
    main()
