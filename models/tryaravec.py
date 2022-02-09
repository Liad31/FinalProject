import gensim
import re
import numpy as np
import torch
from nltk import ngrams

# t_model = gensim.models.Word2Vec.load('full_uni_sg_100_wiki.mdl')
# word_vectors = t_model.wv
# del t_model
# key = 'سلاام'
# print(key in word_vectors)
# vector = word_vectors[key]
# print(vector)
from pandas._libs.internals import defaultdict


def lengths_clones(samples):
    d = {}
    for s in samples:
        if len(s) in d.keys():
            d[len(s)].append(s)
        else:
            d[len(s)] = [s]
    return d


def split_to_batches(samples, batch_size):
    batches = list()
    for size in samples.keys():
        i = 0
        batch = []
        for example in samples[size]:
            if i == batch_size:
                print(batch)
                batches.append(np.array(batch))
                batch = []
                i = 0
            batch.append(example)
            i += 1
        batches.append(np.array(batch))
    return batches


train_df = list()
train_df.append([np.array([0]), np.array([0]), np.array([2])])
train_df.append(list([np.array([0]), np.array([0]), np.array([1])]))
train_df.append(list([np.array([0]), np.array([0])]))
train_df.append(list([np.array([0]), np.array([1])]))
train_df.append(list([np.array([0]), np.array([2])]))
train_df = np.array(train_df, dtype=object)

train = lengths_clones(train_df)
# train_batches = []
# test_batches = []
train_tmp = split_to_batches(train, 2)

print(train)
print(train_df)
print(train_tmp)
