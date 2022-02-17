import numpy as np
import torch
from model import *
from dataprep import *
from config import Config
import random
from early_stopping import EarlyStopping
import nni


def main(config):
    # load data
    data = np.load('train_val.npy', allow_pickle=True)
    train_size = int(0.8 * len(data))
    train_set, val_set = torch.utils.data.random_split(data, [train_size, len(data) - train_size])

    train_iter = split_to_batches(train_set, config.batch_size)
    val_iter = split_to_batches(val_set, config.batch_size)

    # setup model
    model = Seq2SeqAttention(config)
    loss = torch.nn.BCELoss()
    if torch.cuda.is_available():
        model.cuda()
        loss.cuda()
    model.add_optimizer(torch.optim.Adam(model.parameters(), lr=config.lr))
    model.add_loss_op(loss)
    stopper = EarlyStopping(patience=10)

    # train
    for epoch in range(100):
        random.shuffle(train_iter)
        random.shuffle(val_iter)
        model.train()
        model.run_epoch(train_iter, val_iter, epoch)
        model.eval()
        val_acc, val_loss = model.evaluate_model(val_iter)
        stopper(val_loss, model)
        # print("\tVal Accuracy: {:.4f}".format(val_acc))
        nni.report_intermediate_result(val_acc)
        if stopper.early_stop:
            break

    model.load_state_dict(torch.load('checkpoint.pt'))
    val_acc, val_loss = model.evaluate_model(val_iter)
    # print("\t'test' Accuracy: {:.4f}".format(val_acc))
    nni.report_final_result(val_acc)


if __name__ == '__main__':
    params = nni.get_next_parameter()
    config = Config()
    config.set(params)
    main(config)
