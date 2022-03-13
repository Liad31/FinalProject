from model import *
from dataprep import *
import numpy as np
from metrics import *

limit_size = 5
limit_pearson = 0
metric = cut_union_corr_sum

def add_grade(train, train_labels, test, test_lables):
    # prep data
    train_data = get_vids_and_hashtags(train, train_labels)
    train_vid_bucket = train_data
    hash_bucket = to_hashtags_bucket(train_vid_bucket)

    test_data = get_vids_and_hashtags(test, test_lables)

    # setup model
    model = HashtagModel(hash_bucket, train_vid_bucket)

    # train
    model.calc_correlations(limit_size, limit_pearson)

    # predict
    for idx, sample in enumerate(train):
        sample['hash_score'] = model.predict(train_vid_bucket[sample['Vid']][0], metric)
    for sample in test:
        sample['hash_score'] = model.predict(test_data[sample['Vid']][0], metric)
    return train, test


if __name__ == '__main__':
    train = np.load("x_train.npy", allow_pickle=True)
    train_labels = np.load("y_train.npy", allow_pickle=True)
    test = np.load("x_val.npy", allow_pickle=True)
    test_lables = np.load("y_val.npy", allow_pickle=True)
    add_grade(train, train_labels, test, test_lables)
    print("1")