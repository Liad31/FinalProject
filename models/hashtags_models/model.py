import numpy as np
import scipy.stats as sp
import math
from sklearn.metrics import accuracy_score, log_loss, auc, roc_curve
import torch
import os.path as osp
import os
sigmoid = torch.nn.Sigmoid()

# def sigmoid(x):
#     return np.where(x >= 0,
#                     1 / (1 + np.exp(-x)),
#                     np.exp(x) / (1 + np.exp(x)))


class HashtagModel(object):
    def __init__(self, hashtag_bucket=None, vid_bucket=None):
        if hashtag_bucket is None or vid_bucket is None:
            this_dir, this_filename = os.path.split(__file__)
            self.hashtag_bucket = dict(np.load(osp.join(this_dir,"hashtag_bucket.npy"), allow_pickle=True))
            self.vid_bucket = dict(np.load(osp.join(this_dir,"vid_bucket.npy"), allow_pickle=True))
            self.correlations = dict(np.load(osp.join(this_dir,"correlations.npy"), allow_pickle=True))
        else:
            self.hashtag_bucket = hashtag_bucket
            self.vid_bucket = vid_bucket
            self.correlations = None

    def calc_correlations(self, limit_size, limit_pearson):
        correlations = {}
        for hashtag in self.hashtag_bucket:
            if len(self.hashtag_bucket[hashtag]) >= limit_size:
                is_national = []
                is_in_video = []
                for vid in self.vid_bucket:
                    is_in_video.append(1 if hashtag in self.vid_bucket[vid][0] else 0)
                    is_national.append(self.vid_bucket[vid][1])
                pearson = sp.pearsonr(is_national, is_in_video)[0]
                if abs(pearson) >= limit_pearson:
                    correlations[hashtag] = sp.pearsonr(is_national, is_in_video)[0]
        self.correlations = correlations

    def predict(self, x, metric):
        dists = []
        tags = []
        used = []
        for hashtag in x:
            if hashtag in self.correlations:
                for (vid, tag) in self.hashtag_bucket[hashtag]:
                    if vid not in used:
                        dists.append(metric(x, self.vid_bucket[vid][0], self.correlations))
                        tags.append(tag)
        return sigmoid(torch.FloatTensor([np.dot(dists, tags)]))

    def evaluate_auc(self, iterator, metric):
        all_preds = []
        all_y = []
        preds = []
        for example in iterator:
            y_pred = self.predict(example[0], metric)
            all_preds.append(y_pred)
            all_y.append(example[1])
            preds.append(1 if y_pred > 0.5 else -1)
        fpr, tpr, thresholds = roc_curve(all_y, np.array(all_preds).flatten(), pos_label=1)
        acc = accuracy_score(all_y, np.array(preds).flatten())
        return auc(fpr, tpr), acc

    def to_file(self):
        hashtag_bucket = np.array(list(self.hashtag_bucket.items()), dtype=object)
        vid_bucket = np.array(list(self.vid_bucket.items()), dtype=object)
        correlations = np.array(list(self.correlations.items()), dtype=object)
        np.save("hashtag_bucket.npy", hashtag_bucket)
        np.save("vid_bucket.npy", vid_bucket)
        np.save("correlations.npy", correlations)
