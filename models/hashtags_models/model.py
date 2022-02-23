import numpy as np
import scipy.stats as sp
import math
from sklearn.metrics import accuracy_score, log_loss, auc, roc_curve
import torch

sigmoid = torch.nn.Sigmoid()

# def sigmoid(x):
#     return np.where(x >= 0,
#                     1 / (1 + np.exp(-x)),
#                     np.exp(x) / (1 + np.exp(x)))


class HashtagModel(object):
    def __init__(self, hashtag_bucket, vid_bucket):
        self.hashtag_bucket = hashtag_bucket
        self.vid_bucket = vid_bucket
        self.correlations = None

    def calc_correlations(self, limit):
        correlations = {}
        for hashtag in self.hashtag_bucket:
            if len(self.hashtag_bucket[hashtag]) >= limit:
                is_national = []
                is_in_video = []
                for vid in self.vid_bucket:
                    is_in_video.append(1 if hashtag in self.vid_bucket[vid][0] else 0)
                    is_national.append(self.vid_bucket[vid][1])
                correlations[hashtag] = sp.pearsonr(is_national, is_in_video)[0]
        self.correlations = correlations

    def predict(self, x, metric):
        dists = []
        tags = []
        used = []
        for hashtag in x:
            if hashtag in self.hashtag_bucket:
                for (vid, tag) in self.hashtag_bucket[hashtag]:
                    if vid not in used:
                        dists.append(metric(x, self.vid_bucket[vid][0], self.correlations))
                        tags.append(tag)
        return sigmoid(torch.FloatTensor([np.dot(dists, tags)]))

    def evaluate_auc(self, iterator, metric):
        all_preds = []
        all_y = []
        for example in iterator:
            y_pred = self.predict(example[0], metric)
            all_preds.append(y_pred)
            all_y.append(example[1])
        fpr, tpr, thresholds = roc_curve(all_y, np.array(all_preds).flatten(), pos_label=1)
        return auc(fpr, tpr)
