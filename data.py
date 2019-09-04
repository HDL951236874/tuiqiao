Confusion_SimilarPronunciation = {}
Confusion_SimilarShape = {}
with open('data/Pronunciation.txt','r',encoding='UTF-8') as r:
    for i in r:
        l = i[:-1].split('\t')
        Confusion_SimilarPronunciation[l[0]] = l[1:]

import pickle
with open('data/Confusion_SimilarPronunciation.pk', 'wb') as f:
    pickle.dump(Confusion_SimilarPronunciation, f)

with open('data/Shape.txt','r',encoding='UTF_8') as r:
    for i in r:
        l = i[:-1].split(',')
        Confusion_SimilarShape[l[0]] = l[1:]

with open('data/Confusion_SimilarShape.pk', 'wb') as f:
    pickle.dump(Confusion_SimilarShape, f)


