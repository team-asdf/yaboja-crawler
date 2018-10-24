import re
import requests
import json
import time
from bs4 import BeautifulSoup

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


def getKeywords(title):
    dataset = ['c#', 'c', 'c++', 'python', 'python3', 'anaconda', 'django', 'pandas', 'ruby', 
    'java', 'javascript', 'ajax', 'jquery', 'nodejs', 'node.js', 'typescript', 'react', 'rxjs', 'spring', 
    'jsp', 'angular', 'reactnative', 'php', 'json', 'vue', 'graphql', 'apollo', 'prisma', 'nextjs', 'web', 'html', 
    'es', 'css', 'scss', 'sass', 'stylesheet', 'bootstrap', 'material', 'go', 'kotlin', 'r', 'swift', 'xml', 'vhdl', 'verilog', 'systemverilog',
    'unity', 'unreal', 'mysql', 'mongodb', 'nosql', 'ios', 'android', 'ionic', 'cnn', 'rnn', 'lstm', 'blockchain', 'bitcoin', 'ethereum']

    except_hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
    word_of_title = except_hangul.findall(title)

    keywords = []
    # topic_list = []

    for word in word_of_title:
        if word.isalpha():
            # print(word, end='')

            res = requests.get("https://github.com/topics/" + word)
            topic_source = res.text
            topic_soup = BeautifulSoup(topic_source, 'lxml')

            related = topic_soup.find_all("div", {"class": "col-md-4 mt-6 mt-md-0"})
            for r in related:
                topic = r.find_all("a", {"class": "topic-tag"})
                # print(topic)
                for t in topic:
                    #print(t.text.strip())
                    #if t.text.strip() in dataset:
                    #    keywords.append(t.text.strip())

                    # topic_list.append(t.text.strip())

                    # print(" is Keyword")
                    keywords.append(word)
                    # topic_list.clear()
                    break
            # topic_list.clear()

    print(keywords)
    return keywords


def githubTopicSearch(title):
    except_hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
    word_of_title = except_hangul.findall(title)
    # word_of_content = except_hangul.findall(content)
    keywords = []

    for word in word_of_title:
        headers = {'User-Agent': 'Test', "Accept": "application/vnd.github.mercy-preview+json"}
        params = {'q': word + '+is:featured'}
        res = requests.get("https://api.github.com/search/topics", headers=headers, params=params)
        if res.status_code == 403:
            print("403 rate limit")
            time.sleep(60)
            res = requests.get("https://api.github.com/search/topics", headers=headers, params=params)
        result_json = json.loads(res.text)
        # print(res.status_code)
        try:
            idx = 0
            while result_json['items'][idx]['score'] > 500:
                print(result_json['items'][idx]['name'])
                keywords.append(result_json['items'][idx]['name'])
                idx += 1
        except IndexError:
            print("No English words")
        time.sleep(7)
    return keywords
'''
    if not keywords:
        for word in word_of_content:
            headers = {'User-Agent': 'Test', "Accept": "application/vnd.github.mercy-preview+json"}
            params = {'q': word + '+is:featured'}
            res = requests.get("https://api.github.com/search/topics", headers=headers, params=params)
            if res.status_code == 403:
                print("403 rate limit")
                time.sleep(60)
                res = requests.get("https://api.github.com/search/topics", headers=headers, params=params)
            result_json = json.loads(res.text)
            # print(res.status_code)
            try:
                idx = 0
                while result_json['items'][idx]['score'] > 750:
                    print(result_json['items'][idx]['name'])
                    keywords.append(result_json['items'][idx]['name'])
                    idx += 1
            except IndexError:
                print("No English words")
            time.sleep(5)
'''
    # return keywords


if __name__ == "__main__":
    pass