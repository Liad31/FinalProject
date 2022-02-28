from model import *
from dataprep import *
import numpy as np
import sys


class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("logfile.log", "a")

    def write(self, message):
        self.terminal.write(message)
        self.terminal.flush()
        self.log.write(message)
        self.log.flush()

    def flush(self):
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        # you might want to specify some extra behavior here.
        pass


sys.stdout = Logger()


def main(limit_size, limit_pearson, metric):
    # load data
    data = np.load('train_val.npy', allow_pickle=True)
    train_size = int(0.85 * len(data))

    auces = []
    acces = []
    for idx in range(10):
        # prep data
        train_set, val_set = torch.utils.data.random_split(data, [train_size, len(data) - train_size])
        val_iter = dict(val_set).values()
        vid_bucket = dict(train_set)
        hash_bucket = to_hashtags_bucket(vid_bucket)

        # setup model
        model = HashtagModel(hash_bucket, vid_bucket)

        # train
        model.calc_correlations(limit_size, limit_pearson)

        auc, acc = model.evaluate_auc(val_iter, metric)
        print(f'\t\tauc number {idx}: {auc}')
        print(f'\t\tacc number {idx}: {acc}')
        auces.append(auc)
        acces.append(acc)
    auc = np.mean(np.array(auces))
    acc = np.mean(np.array(acces))
    print(f'\tmean auc: {auc}')
    print(f'\tmean acc: {acc}')


def search():
    sys.stdout = Logger()
    pearson_limits = [0.05, 0.1, 0.15, 0.2, 0.4]
    size_limits = [5, 2, 1, 10, 20]
    metrics = {'cut_union_corr_sum': cut_union_corr_sum, 'cut_union_corr': cut_union_corr, 'cut_union': cut_union, 'cut': cut}
    for metric in metrics:
        for size_limit in size_limits:
            for pearson_limit in pearson_limits:
                print(f'starting test on params:\n\tpearson_limit={pearson_limit}\n\tsize_limit={size_limit}\n\tmetric={metric}')
                main(size_limit, pearson_limit, metrics[metric])
                print(f'finishing test on params:\n\tpearson_limit={pearson_limit}\n\tsize_limit={size_limit}\n\tmetric={metric}')



if __name__ == '__main__':
    main(10, 0, union_corr_sum)
