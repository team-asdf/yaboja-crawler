import csv
import pymysql

conn = pymysql.connect(host='localhost',port=3306,user='yaboja',passwd='',db='yaboja',charset='utf8')
cur = conn.cursor()

lst = ["./tech-crawler-ghyeon/csv/update.csv", "./tech-crawler-jungwoo/data/update.csv"]

for each in lst:
    with open(each) as csvfile:
        sp = csv.DictReader(csvfile)
        for row in sp:
            sql = 'insert into contents(`title`, `content`, `url`, `cnt`, `source`, `keyword`, `image`, `createdAt`, `priority`) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")'% (str(row['title']), str(row['content']), str(row['url']), str(row['cnt']), str(row['source']), str(row['keyword']), str(row['image']), str(row['createdAt']), str(row['priority']))
            cur.execute(sql)
    csvfile.close()

conn.commit()
cur.close()

print("done")
