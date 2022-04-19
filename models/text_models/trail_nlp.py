import numpy as np
import torch
from .model import *
from .dataprep import *
from .config import Config
import random
from .early_stopping import EarlyStopping
import nni
import os.path as osp

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


def embed_text2(data, labels):
    config = Config()
    nlp_model = Seq2SeqAttention(config)
    this_dir, this_filename = os.path.split(__file__)
    cuda_available = torch.cuda.is_available()
    mapLoc="cuda:0" if cuda_available else "cpu"
    nlp_model.load_state_dict(torch.load(osp.join(this_dir,'text_model.pt'), map_location=mapLoc))
    embed_text(nlp_model, data, labels)


if __name__ == '__main__':
    # x_train = np.load('../hashtags_models/x_train_new.npy', allow_pickle=True)
    # x_val = np.load('../hashtags_models/x_val.npy', allow_pickle=True)
    # x_test = np.load('../hashtags_models/x_test_new.npy', allow_pickle=True)
    #
    # config = Config()
    # nlp_model = Seq2SeqAttention(config)
    # nlp_model.load_state_dict(torch.load('text_model.pt'))
    # embed_text2(x_train, torch.tensor(np.zeros(len(x_train))))
    # embed_text(nlp_model, x_val, torch.tensor(np.zeros(len(x_val))))
    # embed_text2(x_test, torch.tensor(np.zeros(len(x_test))))
    #
    # np.save("x_train_new.npy", np.array(x_train, dtype=object))
    # np.save("x_val_new.npy", np.array(x_val, dtype=object))
    # np.save("x_test_new.npy", np.array(x_test, dtype=object))
    x_train = np.load('x_train_new.npy', allow_pickle=True)
    # x_val = np.load('x_val_new.npy', allow_pickle=True)
    x_test = np.load('x_test_new.npy', allow_pickle=True)
    # train_test(config)
    print(1)
