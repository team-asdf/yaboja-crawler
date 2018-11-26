import re
import requests
import json
import time
import sys
import os
from bs4 import BeautifulSoup
from summa import keywords, summarizer
from multiprocessing import Manager, Pool


manager = Manager()
L = manager.list()

with open(os.path.dirname(os.path.realpath(__file__)) + "/keywords.json", 'r') as f:
    data = json.load(f)


def englishSummary(content):
    _summaries = summarizer.summarize(content)
    _keywords = keywords.keywords(content, words=5, split=True)

    return _summaries


def getKeywordsForProcess(word):
    global L

    if word.isalpha():
        res = requests.get("https://github.com/topics/" + word)
        topic_source = res.text
        topic_soup = BeautifulSoup(topic_source, 'lxml')

        related = topic_soup.find_all("div", {"class": "col-md-4 mt-6 mt-md-0"})
        for r in related:
            topic = r.find_all("a", {"class": "topic-tag"})
            for t in topic:
                for key in data.keys():
                    if t.text.strip() in data[key]:
                        L.append(t.text.strip())
                        L.append(key)


def getKeywordsForMulti(title, content, source, korean=True):
    global L
    L[:] = [] # delete keyword list L
    # print(L)
    
    except_hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')

    if korean:
        word_of_content = except_hangul.findall(content)
    else:
        summary_text = englishSummary(content)
        word_of_content = except_hangul.findall(summary_text)
    
    word_of_title = except_hangul.findall(title)
    
    words = []

    for t in word_of_title:
        if t.isalpha() and t != source:
            if 3 <= len(t) <= 16:
                words.append(t)

    for t in word_of_content:
        if len(words) > 20:
            break
        if t.isalpha() and t != source:
            if 3 <= len(t) <= 16:
                words.append(t)

    words = list(set(words))
    print(len(words))
    print(words)

    pool = Pool(processes=8)
    pool.map(getKeywordsForProcess, words)
    pool.close()

    print(list(set(L)))
    return list(set(L))


def getKeywords(title, content, source, korean=True):
    ret_list = []
    except_hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')

    if korean:
        word_of_content = except_hangul.findall(content)
    else:
        summary_text = englishSummary(content)
        word_of_content = except_hangul.findall(summary_text)
    
    word_of_title = except_hangul.findall(title)
    
    words = []

    for t in word_of_title:
        if t.isalpha() and t != source:
            if 3 <= len(t) <= 16:
                words.append(t)

    for t in word_of_content:
        if len(words) > 20:
            break
        if t.isalpha() and t != source:
            if 3 <= len(t) <= 16:
                words.append(t)

    words = list(set(words))
    print(len(words))
    print(words)

    for word in words:
        if word.isalpha():
            res = requests.get("https://github.com/topics/" + word)
            topic_source = res.text
            topic_soup = BeautifulSoup(topic_source, 'lxml')

            related = topic_soup.find_all("div", {"class": "col-md-4 mt-6 mt-md-0"})
            for r in related:
                topic = r.find_all("a", {"class": "topic-tag"})
                for t in topic:
                    for key in data.keys():
                        if t.text.strip() in data[key]:
                            ret_list.append(t.text.strip())
                            ret_list.append(key)

    print(list(set(ret_list)))
    return list(set(ret_list))


if __name__ == "__main__":
    pass