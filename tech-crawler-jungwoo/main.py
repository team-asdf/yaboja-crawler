import woowabros
import vingle
import news_feed
import kakao
import netflix
import dropbox
import line
import paypal
import slack
import openai
import alistapart
import lezhin

import os, csv, sys

if __name__ == "__main__":
    multi = False
    if len(sys.argv) == 2 and sys.argv[1] == "--multi":
        multi = True

    updater = open(os.path.dirname(os.path.realpath(__file__)) + "/data/update.csv", "w", encoding='utf-8', newline='')
    updater.close()

    woowabros.main(multi)
    vingle.main(multi)
    kakao.main(multi)
    netflix.main(multi)
    dropbox.main(multi)
    line.main(multi)
    paypal.main(multi)
    slack.main(multi)
    openai.main(multi)
    alistapart.main(multi)
    lezhin.main(multi)
    news_feed.main(multi)

    files = ["woowabros", "vingle", "kakao", "netflix", "dropbox", "line", "paypal", "slack", "openai", "alistapart", "lezhin", "news_feed"]
    merge = open(os.path.dirname(os.path.realpath(__file__)) + "/data/merged.csv", "w", encoding='utf-8', newline='')
    merge_writer = csv.writer(merge)
    merge_writer.writerow(["title", "content", "url", "cnt", "source", "keyword", "image", "createdAt", "priority"])
    for file in files:
        divided = open(os.path.dirname(os.path.realpath(__file__)) + "/data/" + file + ".csv", "r", encoding='utf-8')
        rdr = csv.reader(divided)
        for line in rdr:
            if line[0] == "title": 
                continue
            merge_writer.writerow(line)
        divided.close()
    merge.close()

