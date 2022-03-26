import numpy as np
import re
import gensim
import torch
import random
import scipy.stats as sp
from models.hashtags_models.metrics import *
import math


def sigmoid(x):
    sig = 1 / (1 + math.exp(-x))
    return sig


def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


def get_hashtags(text):
    hashtags = []
    text = remove_emoji(text)
    text = text.replace("#", " # ").strip()
    flag = False
    for word in text.split():
        if flag:
            hashtags.append(word.lower() if word[-1].isnumeric() else word.lower().strip(word[-1]))
            flag = False
        if word == "#":
            flag = True
    return hashtags


def get_vids_and_hashtags(examples, labels):
    # load data
    # examples = np.load("../data.npy", allow_pickle=True)
    # labels = np.load("../tag.npy")
    new_data = [(example['Vid'], example['text'], example['videoText'] if 'videoText' in example else "", 1 if label else -1) for (example, label) in zip(examples, labels)]

    # clean data
    vids_hashtags = {}
    for (video, dis_text, video_text, tag) in new_data:
        hashtags = get_hashtags(dis_text)
        hashtags.extend(get_hashtags(video_text))
        vids_hashtags[video] = (hashtags, tag)
    return vids_hashtags


def to_hashtags_bucket(vids_and_hashtags):
    bucket = {}
    for vid in vids_and_hashtags:
        for hashtag in vids_and_hashtags[vid][0]:
            if hashtag in bucket:
                bucket[hashtag].append((vid, vids_and_hashtags[vid][1]))
            else:
                bucket[hashtag] = [(vid, vids_and_hashtags[vid][1])]
    return bucket


def calc_correlations(limit, bucket, vids):
    correlations = {}
    for hashtag in bucket:
        if len(bucket[hashtag]) >= limit:
            is_national = []
            is_in_video = []
            for vid in vids:
                is_in_video.append(1 if hashtag in vids[vid][0] else 0)
                is_national.append(vids[vid][1])
            correlations[hashtag] = sp.pearsonr(is_national, is_in_video)[0]
    return correlations


def predict(x, hashtag_bucket, vid_bucket, metric, corraletions):
    dists = []
    tags = []
    used = []
    for hashtag in x:
        if hashtag in hashtag_bucket:
            for (vid, tag) in hashtag_bucket[hashtag]:
                if vid not in used:
                    dists.append(metric(x, vid_bucket[vid][0], corraletions))
                    tags.append(tag)
    return sigmoid(np.dot(dists, tags))


if __name__ == '__main__':
    data = dict(np.load("train_val.npy", allow_pickle=True))
    hashtags = to_hashtags_bucket(data)
    coral = calc_correlations(5, hashtags, data)
    pred = predict(data['6960481730042055937'][0], hashtags, data, cut_union, coral)
    print(1)