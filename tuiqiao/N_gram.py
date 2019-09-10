import math
import pickle

class N_gram():
    def __init__(self, N = 5, make_list = False):
        self.N = N
        self.threshold = -10
        self.path = 'tuiqiao/data/data.train'
        self.training_result_path = 'tuiqiao/data/small.pk'

        if make_list:
            self.data = self.make_data_list()

        self.dictionary = self.make_dictionary()
        self.PronunciationConfusion_list = self.Confusion_SimilarPronunciation()
        self.ShapeConfusion_list = self.Confusion_SimilarShape()


    def make_dictionary(self):
        import os
        if os.path.exists('tuiqiao/data/small.pk'):
            with open('tuiqiao/data/small.pk', 'rb') as f:
                data = pickle.load(f)
            return data
        else:
            print('WARNING:YOU DO NOT HAVE A PRETRAINED MODEL PREPARED AND IF YOU WANT TO CONTINUE, PLEASE USE PROCESS FUNCTION!!!')

    def count_gram(self):
        l4d = []
        for i in range(self.N):
            N = self.N
            d = {}
            for idx in self.data:
                for sen in idx[1:]:
                    for j in range(len(sen) - N):
                        if sen[j:j + i + 1] not in d:
                            d[sen[j:j + i + 1]] = 1
                        else:
                            d[sen[j:j + i + 1]] += 1
            l4d.append(d)
        return l4d

    def adjusting(self, l):
        dic_after_ad = []
        for i in range(self.N - 1):
            dic_new = {}
            n_gram_dict = l[i]
            n_1_gram_dict = l[i + 1]
            num = 0
            for j in n_gram_dict:

                if j[0] == 's':
                    dic_new[j] = n_gram_dict[j]
                else:
                    if j not in dic_new:
                        dic_new[j] = 0
                    for k in n_1_gram_dict:
                        if k[1:] == j:
                            dic_new[j] += 1
                num +=1

            dic_after_ad.append(dic_new)
        dic_after_ad.append(l[-1])

        return dic_after_ad


    def count_and_adjusting(self,l):
        d= {} # this is a dictionary for all the gram
        d4gram = [{} for _ in range(self.N)]
        from tqdm import tqdm

        for j in tqdm(range(len(l))):
            for sen in l[j]:
                for i in range(len(sen)):

                    if self.N > len(sen)-i:
                        gram_sen = sen[i:]
                        if gram_sen[0] == 's':
                            for index in range(1,len(gram_sen)+1):
                                if gram_sen[:index] not in d4gram[len(gram_sen[:index])-1]:
                                    d4gram[len(gram_sen[:index])-1][gram_sen[:index]] = 1
                                else:
                                    d4gram[len(gram_sen[:index])-1][gram_sen[:index]] += 1
                    else:
                        gram_sen = sen[i:i+self.N]
                        if gram_sen[0] == 's':
                            for index in range(1,len(gram_sen)+1):
                                if gram_sen[:index] not in d4gram[len(gram_sen[:index])-1]:
                                    d4gram[len(gram_sen[:index])-1][gram_sen[:index]] = 1
                                else:
                                    d4gram[len(gram_sen[:index])-1][gram_sen[:index]] += 1

                        else:
                            if gram_sen not in d4gram[len(gram_sen)-1]:
                                d4gram[len(gram_sen)-1][gram_sen] = 1
                            else:
                                d4gram[len(gram_sen)-1][gram_sen] += 1

                    gram_layer = d
                    for char in gram_sen:
                        if char not in gram_layer:
                            gram_layer[char] = {}
                        gram_layer = gram_layer[char]
        char = ''
        self.tree_function(d,d4gram,char)
        return d4gram,d


    def tree_function(self,d,d4gram,char):
        for key in d:
            char += key
            if char[1:] not in d4gram[len(char)-2] and char[1:] != '':
                d4gram[len(char)-2][char[1:]] = 1
            elif char[1:] != '':
                d4gram[len(char)-2][char[1:]] += 1
            if d[key] != {}:
                self.tree_function(d[key],d4gram,char)
            char = char[:-1]

    def discount(self, l):
        """
        :param l: the list after adjusting
        :return:
        """
        discount = [[0 for _ in range(4)] for __ in range(self.N)]
        for n in range(self.N):
            for k in range(4):
                num = 0
                for key, val in l[n].items():
                    if val == k + 1:
                        num += 1
                discount[n][k] = num

        D = [[0 for _ in range(3)] for __ in range(self.N)]
        for n in range(self.N):
            for k in range(3):
                D[n][k] = k + 1 - (k + 2) * discount[n][0] * discount[n][k + 1] / (
                        (discount[n][0] + 2 * discount[n][1]) * discount[n][k])
        return D, discount

    def process_u(self, l, D, d):
        u = [{} for _ in range(self.N)]
        sum_0 = sum([x[1] for x in l[0].items()]) - l[0]['s']
        for n in range(self.N):
            for key, val in l[n].items():
                if n == 0:
                    Sum = sum_0
                else:
                    char = key[:-1]
                    dic_ = d
                    for sting in char:
                        dic_ = dic_[sting]
                    Sum = 0
                    for k in dic_:
                        Sum += l[n][char+k]

                if val > 3: val = 3
                u[n][key] = (val - D[n][val - 1]) / Sum

        return u,sum_0

    def process_b(self, l, D, discount,Sum_0,d):
        b = [{} for _ in range(self.N - 1)]
        b_ = (D[0][0] *  discount[0][0]+ D[0][1] * discount[0][1] + D[0][2] * discount[0][2]) / Sum_0

        for n in range(self.N - 1):
            for key, val in l[n].items():
                if key[-1] == '~':
                    continue
                char = key
                dic_ = d
                Sum = 0
                for string in char:
                    dic_ = dic_[string]
                num = [0 for _ in range(3)]
                for k in dic_:
                    Sum += l[n+1][char+k]
                    if l[n+1][char+k] == 1:
                        num[0] +=1
                    elif l[n+1][char+k] == 2:
                        num[1] +=1
                    elif l[n+1][char+k] ==3:
                        num[2] +=1

                p1 = D[n+1][0] * num[0]+ D[n+1][1]*num[1] + D[n+1][2]*num[2]
                p2 = Sum
                b[n][key] = p1 / p2

        return b,b_

    def process_p(self, u, b, w, b_, length):
        if len(w) == 1:
            return u[0][w] + b_/length
        else:
            return u[len(w)-1][w] + b[0][w[0]]*self.process_p(u,b,w[1:],b_,length)

    def PROCESS(self):
        l = self.make_data_list()
        after_adjust,d = self.count_and_adjusting(l[:10000])
        after_discount,discount = self.discount(after_adjust)
        U,sum_0 = self.process_u(after_adjust, after_discount,d)
        B, b_ = self.process_b(after_adjust, after_discount,discount,sum_0,d)
        final = [{} for _ in range(self.N)]
        length = len(after_adjust[0])
        for n in range(self.N):
            for key in after_adjust[n]:
                try:
                    score = math.log10(self.process_p(U,B,key,b_,length))
                    final[n][key] = score  if score>-1000 else -1000
                except KeyError:
                    continue
        return final

    def make_data_list(self):
        with open(self.path, 'r', encoding='UTF-8') as op:
            l = []
            for i in op:
                sen = ['s' + x + '~' for x in i[:-1].split('\t')[2:]]
                l.append(sen)

        return l

    def Confusion_SimilarPronunciation(self):
        import os
        if os.path.exists('tuiqiao/data/Confusion_SimilarPronunciation.pk'):
            with open('tuiqiao/data/Confusion_SimilarPronunciation.pk','rb') as f:
                data = pickle.load(f)
            return data

    def Confusion_SimilarShape(self):
        import os
        if os.path.exists('tuiqiao/data/Confusion_SimilarShape.pk'):
            with open('tuiqiao/data/Confusion_SimilarShape.pk','rb') as f:
                data = pickle.load(f)
            return data

    def correct_single_sen_threshold(self,w):

        candidate = []
        char = w[-1]
        if char in self.PronunciationConfusion_list:
            word_list_P = []
            for index in self.PronunciationConfusion_list[char]:
                word_list_P += index
            candidate += word_list_P
        if char in self.ShapeConfusion_list:
            word_list_S = []
            for index in self.ShapeConfusion_list[char]:
                word_list_S += index
            candidate += word_list_S

        # sen = w[:-1]
        max_score = -1000
        max_score_index = ''
        for index in candidate:
            gram_sen = w[:-1] + index
            score = self.dictionary[len(gram_sen)-1][gram_sen] if gram_sen in self.dictionary[len(gram_sen)-1] else -1000
            if score >max_score:
                max_score = score
                max_score_index = index

        return max_score_index if max_score_index!=0 else ''

    def correct_single_sen_brute_froce(self,w):
        candidate_for_each_word = []
        for i in range(len(w)):
            candidate = []
            if w[i] in self.PronunciationConfusion_list:
                word_list_P = []
                for index in self.PronunciationConfusion_list[w[i]]:
                    word_list_P += index
                candidate += word_list_P
            if w[i] in self.ShapeConfusion_list:
                word_list_S = []
                for index in self.ShapeConfusion_list[w[i]]:
                    word_list_S += index
                candidate += word_list_S
            for j in candidate:
                if j not in self.dictionary[0]:
                    candidate.remove(j)
                    continue
                if i == 0:
                    if j+w[i+1] not in self.dictionary[1]:
                        candidate.remove(j)
                        continue
                if i == len(w) - 1:
                    if w[i-1] + j not in self.dictionary[1]:
                        candidate.remove(j)
                        continue
                if i != 0 and i != len(w) -1:
                    if w[i-1] + j not in self.dictionary[1] and j+w[i+1] not in self.dictionary[1]:
                        candidate.remove(j)
                        continue

            candidate_for_each_word.append(candidate)

        return candidate_for_each_word

    def correct_single_sen(self,w):
        # Sen_Score = 0
        w = 's'+w+'~'
        after_correct = ''
        for i in range(1,len(w)+1):
            sen = w[:i] if i<self.N else w[i-self.N:i]
            score = self.dictionary[len(sen)-1][sen] if sen in self.dictionary[len(sen)-1] else -1000
            if score < self.threshold:
                new_word = self.correct_single_sen_threshold(sen)
                if new_word != '':
                    w = w[:i-1]+new_word+w[i:]
            else:
                new_word = sen[-1]
            # Sen_Score += score
            after_correct += new_word
        return after_correct[1:-1]

    def save_model(self,res):
        import pickle
        with open(self.training_result_path, 'wb') as f:
            pickle.dump(res, f)


def pack_up(data):
    import pickle
    with open('tuiqiao/data/small.pk', 'wb') as f:
        pickle.dump(data, f)


def loading():
    import pickle
    with open('tuiqiao/data/checkpoint.pk', 'rb') as f:
        data = pickle.load(f)
    return data

# test_ = [['s我~'],
#          ['s你我~'],
#          ['s他~'],
#          ['s我~'],
#          ['s你~']]

if __name__ == '__main__':
    M = N_gram(5)
    test = '今田添气不好。'
    l = M.correct_single_sen(test)
