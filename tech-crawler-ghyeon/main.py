import os
import csv
import time
import sys


from crawl_luavis_kr import Luavis
from crawl_subicura_com import Subicura
from crawl_mingrammer_com import Mingrammer
from crawl_taetaetae_github_io import Tae


def main():
    start = time.time()
    if len(sys.argv) == 2 and sys.argv[1] == "--full":
        print("Full ", end="")
        try:
            os.remove("./csv/main.csv")
        except FileNotFoundError:
            pass
        try:
            os.remove("./csv/update.csv")
        except FileNotFoundError:
            pass

    else:
        print("Update ", end="")
        merge_update()
    print("Operation Start")
    crawl_list = [Luavis(), Subicura(), Mingrammer(), Tae()]
    for each in crawl_list:
        each.main()
    if len(sys.argv) == 2 and sys.argv[1] == "--full":
        make_main()
    else:
        make_update()
    print("Operation End")
    print("Time Elapsed:", int(time.time() - start))


def merge_update():
    # merge update to main file
    to_update = []
    try:
        update = open("./csv/update.csv", "r", encoding="utf-8")
    except FileNotFoundError:
        pass
    else:
        in_update = list(csv.reader(update))
        for idx in range(1, len(in_update)):
            to_update.append(in_update[idx])
        update.close()
    try:
        main_file = open("./csv/main.csv", "a", encoding="utf-8")
    except FileNotFoundError:
        print("main.csv not found. make main.csv")
        make_main()
    else:
        writer = csv.writer(main_file)
        for each in to_update:
            writer.writerow(each)
        main_file.close()
    try:
        os.remove("./csv/update.csv")
    except FileNotFoundError:
        pass


def make_update():
    # make new update file
    csv_list = []
    for file in os.listdir("./csv"):
        if file.endswith(".csv"):
            if file != "main.csv" and file != "update.csv":
                csv_list.append(file)

    main_file = open("./csv/main.csv", "r", encoding="utf-8")
    main_list = list(csv.reader(main_file))
    main_file.close()

    temp_lst = list()
    temp_lst.append(["title", "content", "url", "cnt", "source", "keyword", "image", "createdAt", "priority"])
    for file in csv_list:
        raw = open("./csv/" + file, "r", encoding="utf-8")
        lst = list(csv.reader(raw))
        for idx in range(1, len(lst)):
            if lst[idx] not in main_list:
                temp_lst.append(lst[idx])
        raw.close()

    write = open("./csv/update.csv", "w", encoding="utf-8")
    writer = csv.writer(write)
    for each in temp_lst:
        writer.writerow(each)
    write.close()


def make_main():
    csv_list = []
    for file in os.listdir("./csv"):
        if file.endswith(".csv"):
            if file != "main.csv":
                csv_list.append(file)

    temp_lst = list()
    temp_lst.append(["title", "content", "url", "cnt", "source", "keyword", "image", "createdAt", "priority"])
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


if __name__ == "__main__":
    main()
