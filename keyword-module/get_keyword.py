import re
import requests
import json
import time
import sys
from bs4 import BeautifulSoup
from lexrankr import LexRank
from multiprocessing import Process, Manager


##############################################
# TODO
# 한글 단어 -> 영어 단어 변환
# 정확도 어느정도 OK, but 속도 너무 느림
##############################################

#----------------------------------------------
# github 토픽 존재 -> 유효성 확인?

# 1. 제목에서 명사 추출 / 정규식으로 영단어 추출 O
# 2. 검색결과를 통해서 유효성 확인 O
# 3. 유효하다면 키워드로 사용 O
# 4. 유효하지 않다면 컨텐츠에서 영단어 추출
#----------------------------------------------

#----------------------------------------------
# by Github API
# 단어 검색 -> 유사성 점수 500이상인 토픽 -> 유효한 키워드로 인정
#----------------------------------------------

dataset = ['c#', 'c', 'c++', 'python', 'python3', 'anaconda', 'django', 'pandas', 'ruby', 
    'java', 'javascript', 'ajax', 'jquery', 'nodejs', 'node.js', 'typescript', 'react', 'reactjs', 'react.js', 'rxjs', 'spring', 
    'angular', 'angularjs', 'angular.js', 'jsp', 'angular', 'reactnative', 'php', 'json', 'vue', 'vue.js', 'vuejs', 'graphql', 'apollo', 'prisma', 
    'nextjs', 'web', 'html', 'es', 'css', 'scss', 'sass', 'stylesheet', 'bootstrap', 'material', 'go', 'kotlin', 'r', 'swift', 
    'xml', 'vhdl', 'verilog', 'systemverilog', 'unity', 'unreal', 'mysql', 'mongodb', 'nosql', 'ios', 'android', 'ionic', 
    'cnn', 'rnn', 'lstm', 'blockchain', 'bitcoin', 'ethereum']


def summary(content):
    lexrank = LexRank()  # can init with various settings
    
    lexrank.summarize(content)
    summaries = lexrank.probe(None)  # `num_summaries` can be `None` (using auto-detected topics)
    _summaries = "\n".join(summaries)

    return _summaries


def printProgress(iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100): 
    formatStr = "{0:." + str(decimals) + "f}" 
    percent = formatStr.format(100 * (iteration / float(total))) 
    filledLength = int(round(barLength * iteration / float(total))) 
    bar = '■' * filledLength + '-' * (barLength - filledLength) 
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)), 
    if iteration == total: 
        sys.stdout.write('\n') 
    sys.stdout.flush()


def getKeywords_for_process(L, word):
    if word.isalpha():
        res = requests.get("https://github.com/topics/" + word)
        topic_source = res.text
        topic_soup = BeautifulSoup(topic_source, 'lxml')

        related = topic_soup.find_all("div", {"class": "col-md-4 mt-6 mt-md-0"})
        for r in related:
            topic = r.find_all("a", {"class": "topic-tag"})
            for t in topic:
                if t.text.strip() in dataset:
                    L.append(t.text.strip())


def getKeywords_multi(title, content):
    except_hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
    word_of_title = except_hangul.findall(title)

    summary_text = summary(content)
    word_of_content = except_hangul.findall(summary_text)

    with Manager() as manager:
        L = manager.list()  # <-- can be shared between processes.
        processes = []

        i = 0
        for word in word_of_content:
            p = Process(target=getKeywords_for_process, args=(L, word))  # Passing the list
            p.start()
            processes.append(p)
            i += 1
            printProgress(i, len(word_of_content), 'Content Keyword Progress:', 'Complete', 1, 50)
        for p in processes:
            p.join()

        i = 0
        for word in word_of_title:
            p = Process(target=getKeywords_for_process, args=(L, word))  # Passing the list
            p.start()
            processes.append(p)
            i += 1
            printProgress(i, len(word_of_title), 'Title Keyword Progress:', 'Complete', 1, 50)
        for p in processes:
            p.join()

        print(list(set(L)))
        return list(set(L))


if __name__ == "__main__":
    pass