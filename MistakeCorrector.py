#!/usr/bin/env python
# encoding: utf-8
"""
@author: Dong Jun
@file: mistakeCorrector.py
@time: 2019/8/24 17:00
"""

import json
from TrieTree import Trie
from datetime import datetime

class MistakeCorrector():
    """错别字表里去除了同音的部分，只保留字形相近容易混淆的，同音字可以在拼音部分检测。"""
    def __init__(self, word):
        self.word = word
        self.word_candidate = []
        self.mistake_dict_path = "data/mistake.model"
        self.mistake_dict = self.loadModel(self.mistake_dict_path)
        self.userdict_load = False
        self.userdict_path = ""             # 用于向trie树中添加字典
        self.before_time = datetime.now()
        self.after_time = datetime.now()


    @classmethod
    def loadModel(cls, mistake_dict_path):
        with open(mistake_dict_path, "r", encoding="utf-8") as f:
            mistake_dict = json.load(f)
        return mistake_dict


    def delta_time_calculate(self):
        self.after_time = datetime.now()
        delta_time = self.after_time - self.before_time
        self.before_time = datetime.now()
        return delta_time


    def word_edit(self, word):
        word_edit_list = []
        for i in range(len(word) - 1):
            word_transposition = word[0:i] + word[i + 1] + word[i] + word[i + 2:]
            word_edit_list.append(word_transposition)       # 去掉trie树的判断部分
        return word_edit_list


    def wordCandidate(self):
        mistake_list = []
        word_candidate_list = []
        for w in self.word:
            mistake_list.append(set(self.mistake_dict.get(w, w)))

        # 用深度遍历求候选词的排列组合
        N = len(mistake_list)
        def DFS(per, depth):
            if depth == N:
                word_candidate_list.append(per)         # 去掉trie树的判断部分
            else:
                for w in mistake_list[depth]:
                    DFS(per + w, depth + 1)
        DFS("", 0)
        self.word_candidate.extend(word_candidate_list)
        self.word_candidate.extend(self.word_edit(self.word))       # 只考虑error的编辑距离替换词


    @classmethod
    def build_model(cls):
        mistakeDict = {}
        mistakeList = ["白自", "建延廷", "台合", "洽冶", "申由甲田", "熊能", "习刁匀勺", "崇祟", "今令", "日曰目"]
        with open("data/mistake.model", "w", encoding="utf-8") as f:
            for line in mistakeList:
                for w in line:
                    mistakeDict[w] = line
            f.write(json.dumps(mistakeDict, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    MistakeCorrector.build_model()
    example = MistakeCorrector("白天")
    example.wordCandidate()
    print(example.word_candidate)

