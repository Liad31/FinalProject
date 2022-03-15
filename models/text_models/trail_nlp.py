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
    data = np.load('train_val_300_sg.npy', allow_pickle=True)
    train_size = int(0.85 * len(data))

    auces = []
    ephoces = []
    for idx in range(10):
        # prep data
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
        stopper = EarlyStopping(patience=config.patience)

        # train
        for epoch in range(200):
            random.shuffle(train_iter)
            random.shuffle(val_iter)
            model.train()
            model.run_epoch(train_iter, val_iter, epoch)
            model.eval()
            val_acc, val_loss = model.evaluate_model(val_iter)
            val_auc = model.evaluate_auc(val_iter)
            train_auc = model.evaluate_auc(train_iter)
            print(f'epoch num {epoch}:')
            print(f'train auc: {train_auc}')
            print(f'valid auc: {val_auc}')
            stopper(val_loss, model, save=False)
            if stopper.early_stop:
                ephoces.append(epoch)
                break

        auc = model.evaluate_auc(val_iter)
        print(f'auc number {idx}: {auc}')
        auces.append(auc)
    auc = np.mean(np.array(auces))
    ephoce_mean = np.mean(np.array(ephoces))
    print(f'mean auc: {auc}')
    print(f'mean ephoc: {ephoce_mean}')
    nni.report_final_result(auc)


def train_test(config):
    # load data
    train = np.load('train.npy', allow_pickle=True)
    test = np.load('test.npy', allow_pickle=True)
    # print(len(data))
    # print(len(test))

    # prep data
    train_iter = split_to_batches(train, config.batch_size)
    test_iter = split_to_batches(test, config.batch_size)

    # setup model
    model = Seq2SeqAttention(config)
    loss = torch.nn.BCELoss()
    if torch.cuda.is_available():
        model.cuda()
        loss.cuda()
    model.add_optimizer(torch.optim.Adam(model.parameters(), lr=config.lr))
    model.add_loss_op(loss)

    for epoch in range(15):
        random.shuffle(train_iter)
        model.train()
        model.run_epoch(train_iter, None, epoch)
        model.eval()
        train_auc = model.evaluate_auc(train_iter)
        print(f'epoch num {epoch}:')
        print(f'train auc: {train_auc}')

    model.eval()
    test_auc = model.evaluate_auc(test_iter)
    print(f'test auc: {test_auc}')
    torch.save(model.state_dict(), "text_model.pt")


if __name__ == '__main__':
    # params = nni.get_next_parameter()
    config = Config()
    # config.set(params)
    train_test(config)
