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

import os, csv

if __name__ == "__main__":
    updater = open(os.path.dirname(os.path.realpath(__file__)) + "/data/update.csv", "w", encoding='utf-8', newline='')
    updater.close()

    woowabros.main()
    vingle.main()
    kakao.main()
    netflix.main()
    dropbox.main()
    line.main()
    paypal.main()
    slack.main()
    openai.main()
    alistapart.main()
    lezhin.main()
    news_feed.main()

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

