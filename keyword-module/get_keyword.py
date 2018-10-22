# from konlpy.tag import Kkma
# from konlpy.tag import Twitter
# from konlpy.utils import pprint
import re
import requests
import json
import time
from bs4 import BeautifulSoup

# TODO
# 한글 단어 -> 영어 단어 변환


#----------------------------------------------
# github 토픽 존재 -> 유효성 확인?

# 1. 제목에서 명사 추출 / 정규식으로 영단어 추출 O
# 2. 검색결과를 통해서 유효성 확인 O
# 3. 유효하다면 키워드로 사용 O
# 4. 유효하지 않다면 컨텐츠에서 영단어 추출
#----------------------------------------------


# title = "Texture Best Practice".lower()

# frequency = {}

# spliter = Twitter()
# nouns = spliter.nouns(title)
# pprint(nouns)

def getKeywords(title):
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
                for t in topic:
                    # print(t.text.strip())
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
    keywords = []

    for word in word_of_title:
        headers = {'User-Agent': 'Test', "Accept": "application/vnd.github.mercy-preview+json"}
        params = {'q': word + '+is:curated'}
        res = requests.get("https://api.github.com/search/topics", headers=headers, params=params)
        result_json = json.loads(res.text)
        print(res.status_code)
        try:
            if result_json['items'][0]['score'] > 500:
                print(result_json['items'][0]['name'])
                keywords.append(word)
        except IndexError:
            print("No English words")
        time.sleep(8)

    return keywords

if __name__ == "__main__":
    githubTopicSearch("Search Service in Serverless Architecture")


# print(result)

# match_pattern = re.findall(r'\b[a-z]{3,20}\b', title) # 3~20글자 사이의 영단어 정규식으로 추출
# pprint(match_pattern)

'''
for word in word_of_title:
    if word.isalpha():
        count = frequency.get(word, 0)
        frequency[word] = count + 1

sorted_dict = sorted(frequency.items(), key=lambda x:x[1], reverse=True) # 단어 Count순으로 정렬

for words, count in sorted_dict:
    if(count > 0):
        print(words, count)

        topic_list = []

        res = requests.get("https://github.com/topics/" + words)
        topic_source = res.text
        topic_soup = BeautifulSoup(topic_source, 'lxml')

        related = topic_soup.find_all("div", {"class": "col-md-4 mt-6 mt-md-0"})
        for r in related:
            topic = r.find_all("a", {"class": "topic-tag"})
            for t in topic:
                # print(t.text.strip())
                topic_list.append(t.text.strip())

        if not topic_list:
            print("it is not keyword")
'''




