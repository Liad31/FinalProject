from model import *
from dataprep import *
import numpy as np


def main(limit, metric):
    # load data
    data = np.load('train_val.npy', allow_pickle=True)
    train_size = int(0.85 * len(data))

    auces = []
    ephoces = []
    for idx in range(10):
        # prep data
        train_set, val_set = torch.utils.data.random_split(data, [train_size, len(data) - train_size])
        val_iter = dict(val_set).values()
        vid_bucket = dict(train_set)
        hash_bucket = to_hashtags_bucket(vid_bucket)

        # setup model
        model = HashtagModel(hash_bucket, vid_bucket)

        # train
        model.calc_correlations(limit)

        auc = model.evaluate_auc(val_iter, metric)
        print(f'auc number {idx}: {auc}')
        auces.append(auc)
    auc = np.mean(np.array(auces))
    print(f'mean auc: {auc}')


if __name__ == '__main__':
    main(5, cut)