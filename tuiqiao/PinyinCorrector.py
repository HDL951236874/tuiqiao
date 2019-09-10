#!/usr/bin/env python
# encoding: utf-8
"""
@author: Dong Jun
@file: pinyinCorrector.py
@time: 2019/8/24 10:00
"""

from pypinyin import lazy_pinyin
import json
from datetime import datetime


class PinyinCorrector():
    def __init__(self, word):
        self.word = word
        self.word_candidate = []
        self.pinyin_dict_path = "data/pinyin2word.model"
        self.pinyin_set_path = "data/pinyin_set.model"
        self.pinyin_dict, self.pinyin_set = self.loadModel(self.pinyin_dict_path, self.pinyin_set_path)
        self.before_time = datetime.now()
        self.after_time = datetime.now()


    @classmethod
    def loadModel(cls, pinyin_dict_path, pinyin_set_path):
        with open(pinyin_dict_path, "r", encoding="utf-8") as f:
            pinyin_dict = json.load(f)
        with open(pinyin_set_path, "r", encoding="utf-8") as f:
            pinyin_set = set([line.split("\n")[0] for line in f.readlines()])
        return pinyin_dict, pinyin_set


    def delta_time_calculate(self):
        self.after_time = datetime.now()
        delta_time = self.after_time - self.before_time
        self.before_time = datetime.now()
        return delta_time


    def pinyinEdit(self, pinyin):
        '''返回编辑距离为1以内的增删改操作的拼音集合，并且用交集的方法去掉明显不合理的拼音'''
        n = len(pinyin)
        charList = [chr(i) for i in range(97, 123)]
        pinyin_edit = set([pinyin[0:i] + pinyin[i + 1:] for i in range(n)] +                                   # deletion
                          [pinyin[0:i] + pinyin[i + 1] + pinyin[i] + pinyin[i + 2:] for i in range(n - 1)] +   # transposition
                          [pinyin[0:i] + c + pinyin[i + 1:] for i in range(n) for c in charList] +             # alteration
                          [pinyin[0:i] + c + pinyin[i:] for i in range(n + 1) for c in charList])              # insertion
        return self.pinyin_set & pinyin_edit


    def pinyinCandidate(self, word_pinyin):
        pinyin_candidate = [','.join(word_pinyin)]
        # 将每一个拼音编辑距离为1以内的拼音都记录下来
        pinyin_edit_list = []
        for one_pinyin in word_pinyin:
            pinyin_edit = self.pinyinEdit(one_pinyin)
            pinyin_edit_list.append(pinyin_edit)

        # 用深度遍历求候选拼音的排列组合
        N = len(pinyin_edit_list)
        def DFS(per, depth):
            if depth == N:
                pinyin_candidate.append(per[1:])
            else:
                for w in pinyin_edit_list[depth]:
                    DFS(per + "," + w, depth + 1)
        DFS("", 0)
        return pinyin_candidate


    def wordCandidateSearch(self, pinyin_candidate):
        for pinyin in pinyin_candidate:
            wordsDict = self.pinyin_dict.get(pinyin, {})
            self.word_candidate.extend(wordsDict)


    def wordCandidate(self):
        '''这里用候选拼音查表生成候选词语'''
        word_pinyin = lazy_pinyin(self.word)
        pinyin_candidate = self.pinyinCandidate(word_pinyin)
        self.wordCandidateSearch(pinyin_candidate)


    @classmethod
    def build_model(cls):
        pinyin_set = set({})
        word_dict = {}
        count = 0
        for line in open('data/dict.txt', "r", encoding="utf-8"):
            count += 1
            line = line.strip().split(' ')
            word = line[0]
            word_count = line[1]
            for pinyin in lazy_pinyin(word):
                pinyin_set.add(pinyin)
            word_pinyin = ','.join(lazy_pinyin(word))
            if word_pinyin not in word_dict:
                word_dict[word_pinyin] = word + '_' + word_count
            else:
                word_dict[word_pinyin] += ';' + word + '_' + word_count

        data = {}
        for pinyin, words in word_dict.items():
            tmp = {}
            for word in words.split(';'):
                word_word = word.split('_')[0]
                word_count = int(word.split('_')[1])
                tmp[word_word] = word_count
            data[pinyin] = tmp

        with open('data/pinyin2word.model', 'w', encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False))
        with open('data/pinyin_set.model', 'a', encoding="utf-8") as f:
            for line in list(pinyin_set):
                f.write(line+"\n")


if __name__ == "__main__":
    # PinyinCorrector.build_model()
    example = PinyinCorrector("白天")
    example.wordCandidate()
    print(example.word_candidate)
