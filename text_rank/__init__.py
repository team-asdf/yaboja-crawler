import networkx
import re


class RawTaggerReader:
    def __init__(self, file_path, tagger=None):
        if tagger:
            self.tagger = tagger
        else:
            from konlpy.tag import Komoran
            self.tagger = Komoran(userdic='./text_rank/dic.txt')
        self.file_path = file_path
        self.rgxSplitter = re.compile('([.!?:](?:["\']|(?![0-9])))')

    def __iter__(self):
        for line in open(self.file_path, encoding='utf-8'):
            ch = self.rgxSplitter.split(line)
            for s in map(lambda a, b: a + b, ch[::2], ch[1::2]):
                if not s: 
                    continue
                yield self.tagger.pos(s)


class TextRank:
    def __init__(self, **kwargs):
        self.graph = None
        self.window = kwargs.get('window', 5)
        self.coefficient = kwargs.get('coefficient=', 1.0)
        self.threshold = kwargs.get('threshold', 0.005)
        self.dictCount = {}
        self.dictBiCount = {}
        self.dictNear = {}
        self.nTotal = 0

    def load(self, sentence_iter, word_filter=None):
        def insert_pair(a, b):
            if a > b:
                a, b = b, a
            elif a == b:
                return
            self.dictBiCount[a, b] = self.dictBiCount.get((a, b), 0) + 1

        def insert_near_pair(a, b):
            self.dictNear[a, b] = self.dictNear.get((a, b), 0) + 1

        for sent in sentence_iter:
            for i, word in enumerate(sent):
                if word_filter and not word_filter(word): 
                    continue
                self.dictCount[word] = self.dictCount.get(word, 0) + 1
                self.nTotal += 1
                if i - 1 >= 0 and (not word_filter or word_filter(sent[i - 1])):
                    insert_near_pair(sent[i - 1], word)
                if i + 1 < len(sent) and (not word_filter or word_filter(sent[i + 1])):
                    insert_near_pair(word, sent[i + 1])
                for j in range(i + 1, min(i + self.window + 1, len(sent))):
                    if word_filter and not word_filter(sent[j]): 
                        continue
                    if sent[j] != word:
                        insert_pair(word, sent[j])

    def get_pmi(self, a, b):
        import math
        co = self.dictNear.get((a, b), 0)
        if not co:
            return None
        return math.log(float(co) * self.nTotal / self.dictCount[a] / self.dictCount[b])

    def get_i(self, a):
        import math
        if a not in self.dictCount:
            return None
        return math.log(self.nTotal / self.dictCount[a])

    def build(self):
        self.graph = networkx.Graph()
        self.graph.add_nodes_from(self.dictCount.keys())
        for (a, b), n in self.dictBiCount.items():
            self.graph.add_edge(a, b, weight=n * self.coefficient + (1 - self.coefficient))

    def rank(self):
        return networkx.pagerank(self.graph, weight='weight')

    def extract(self, ratio=0.1):
        ranks = self.rank()
        cand = sorted(ranks, key=ranks.get, reverse=True)[:int(len(ranks) * ratio)]
        print(cand)
        pairness = {}
        start_of = {}
        tuples = {}
        for k in cand:
            tuples[(k,)] = self.get_i(k) * ranks[k]
            for l in cand:
                if k == l:
                    continue
                pmi = self.get_pmi(k, l)
                if pmi:
                    pairness[k, l] = pmi

        for (k, l) in sorted(pairness, key=pairness.get, reverse=True):
            if k not in start_of:
                start_of[k] = (k, l)

        for (k, l), v in pairness.items():
            pmis = v
            rs = ranks[k] * ranks[l]
            path = (k, l)
            tuples[path] = pmis / (len(path) - 1) * rs ** (1 / len(path)) * len(path)
            last = l
            while last in start_of and len(path) < 7:
                if last in path:
                    break
                pmis += pairness[start_of[last]]
                last = start_of[last][1]
                rs *= ranks[last]
                path += (last,)
                tuples[path] = pmis / (len(path) - 1) * rs ** (1 / len(path)) * len(path)

        used = set()
        both = {}
        for k in sorted(tuples, key=tuples.get, reverse=True):
            if used.intersection(set(k)):
                continue
            both[k] = tuples[k]
            for w in k:
                used.add(w)

        return both
