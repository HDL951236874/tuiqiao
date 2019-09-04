#!/usr/bin/env python
# encoding: utf-8
"""
@author: Dong Jun
@file: TrieTree.py
@time: 2019/8/24 19:20
"""

import json
import re

class Trie():
    def __init__(self):
        self.root = self.trie_load()
        self.end = "end"


    def insert(self, word):
        curNode = self.root
        for c in word:
            if not c in curNode:
                curNode[c] = {}
            curNode = curNode[c]
        curNode[self.end] = True


    def search(self, word):
        curNode = self.root
        for c in word:
            if c not in curNode:
                return False
            curNode = curNode[c]
        # Doesn't end here
        if not self.end in curNode:
            return False
        return True


    def startsWith(self, prefix):
        curNode = self.root
        for c in prefix:
            if not c in curNode:
                return False
            curNode = curNode[c]
        return True


    def trie_save(self, word_list):
        for word in word_list:
            self.insert(word)
        with open("data/trie.model", "w", encoding="utf-8") as f:
            f.write(json.dumps(self.root, ensure_ascii=False))


    def trie_load(self):
        try:
            with open("data/trie.model", "r", encoding="utf-8") as f:
                trie_dict = json.load(f)
            return trie_dict
        except:
            return {}


    def load_userdict(self, word_path, save_dict=False):
        with open(word_path, "r", encoding="utf-8") as f:
            for line in f.readlines():
                word = re.split("[\t ]", line)[0]
                self.insert(word)
        if save_dict == True:
            with open("data/trie.model", "w", encoding="utf-8") as f:
                f.write(json.dumps(self.root, ensure_ascii=False))


if __name__ == "__main__":
    example = Trie()
    # example.load_userdict("data/dict.txt", save_dict=True)
    print(example.search("桌子"))
    print(example.search("张三"))
