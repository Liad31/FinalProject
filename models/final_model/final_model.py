import json
import torch
from torch import nn
from torch.nn import functional as F
from sklearn.metrics import accuracy_score, log_loss, auc, roc_curve
import os
import  numpy as np
import pandas as pd
import torch.optim as optim
from tqdm import tqdm
from models.text_models.config import Config
import torch.utils.data as data_utils
from sklearn.model_selection import train_test_split
from sklearn import metrics
from torchvision import datasets, models, transforms
from  models.final_model.dataset import  postsDataset
import matplotlib.pyplot as plt
from models.hashtags_models import  get_hash_score
from  models.text_models import model as nlp
from  models.text_models import dataprep
from  models.audio import get_train_sounds
class postsModel(nn.Module):
    def __init__(self,dropout_squeeze_fc=0, dropout_final_fc=0):
        super().__init__()
        self.video_embed_size = 2048
        self.text_embed_size = 128
        self.video_size = 30
        self.text_size = 16
        self.hash_score_size = 1
        self.sound_size = 1
        self.final_fc_input_size = self.video_size + self.hash_score_size + self.text_size + self.sound_size

        self.squeeze_video = nn.Sequential(
            nn.Linear(int(self.video_embed_size), int(self.video_embed_size/2)),
            nn.BatchNorm1d(int(self.video_embed_size/2)),
            nn.ReLU(),
            nn.Dropout(p=dropout_squeeze_fc),
            nn.Linear(int(self.video_embed_size/2), int(self.video_embed_size /16)),
            nn.BatchNorm1d(int(self.video_embed_size / 16)),
            nn.ReLU(),
            nn.Dropout(p=dropout_squeeze_fc),
            nn.Linear(int(self.video_embed_size / 16), 16),
            nn.BatchNorm1d(16),
        )

        self.squeeze_text =  nn.Sequential(
            nn.Linear(int(self.text_embed_size), int(self.text_embed_size/8)),
            nn.BatchNorm1d(int(self.text_embed_size/8)),
            nn.ReLU(),
            nn.Dropout(p=dropout_squeeze_fc),
            nn.BatchNorm1d(16),
        )

        self.final_fc = nn.Sequential(
            nn.Linear(int(self.final_fc_input_size), int(2* self.final_fc_input_size)),
            nn.BatchNorm1d(int(2* self.final_fc_input_size)),
            nn.ReLU(),
            nn.Dropout(p=dropout_final_fc),
            nn.Linear(int(2* self.final_fc_input_size), 1),
            nn.Sigmoid()
        )

        self.final_fc_no_text = nn.Sequential(
            nn.Linear(int(self.final_fc_input_size-self.text_size), int(2* (self.final_fc_input_size-self.text_size))),
            nn.BatchNorm1d(int(2* (self.final_fc_input_size-self.text_size))),
            nn.ReLU(),
            nn.Dropout(p=dropout_final_fc),
            nn.Linear(int(2* (self.final_fc_input_size-self.text_size)), 1),
            nn.Sigmoid()
        )
        self.dumb = nn.Sequential(
            nn.Linear(2048,1),
            nn.Sigmoid()
        )

    def forward(self, post):
        video_embeded = post['video_embeded'].float()
        # squeezed_video_embeded = self.squeeze_video(video_embeded)
        squeezed_video_embeded = video_embeded

        if post['text'][0]:
            text_embeded = post['text_embeded'].float()
            squeezed_text_embeded = self.squeeze_text(text_embeded)


        hashtags_score = post['hashtags_score'].float().reshape(-1,1)
        sounds_score = post['sound'].float().reshape(-1,1)

        final_tensor = squeezed_video_embeded
        if post['text'][0]:
            final_tensor = torch.concat((final_tensor, squeezed_text_embeded,hashtags_score, sounds_score), dim=-1)
            out = self.final_fc(final_tensor)
        else:
            if len(final_tensor.shape)==1:
                final_tensor = final_tensor.reshape(1,-1)
            final_tensor = torch.concat((final_tensor, hashtags_score, sounds_score), dim=-1)
            out = self.final_fc_no_text(final_tensor)

        return out


def split_batch(batch, labels):
    batch1 = {'video_embeded':torch.tensor([]),'text_embeded':torch.tensor([]),'text':torch.tensor([0]),'sound':torch.tensor([0]),'hashtags_score':torch.tensor([0])}
    batch2 =  {'video_embeded':torch.tensor([]),'text_embeded':torch.tensor([]),'text':torch.tensor([0]),'sound':torch.tensor([0]),'hashtags_score':torch.tensor([0])}
    labels1 = torch.tensor([0])
    labels2 = torch.tensor([0])
    for i in range(len(batch['text'])):
        if batch['text'][i] == 0:
            batch1['video_embeded'] = torch.concat((batch1['video_embeded'], torch.unsqueeze(batch['video_embeded'][i],0)),0)
            batch1['text_embeded'] = torch.concat((batch1['text_embeded'], torch.unsqueeze(batch['text_embeded'][i],0)),0)
            batch1['text'] = torch.concat((batch1['text'], torch.tensor([batch['text'][i]])),0)
            batch1['sound'] = torch.concat((batch1['sound'], torch.tensor([batch['sound'][i]])),0)
            batch1['hashtags_score'] = torch.concat((batch1['hashtags_score'], torch.tensor([batch['hashtags_score'][i]])),0)
            labels1 = torch.concat((labels1, torch.tensor([labels[i]])),0)
        else:
            batch2['video_embeded'] = torch.concat((batch2['video_embeded'], torch.unsqueeze(batch['video_embeded'][i],0)),0)
            batch2['text_embeded'] = torch.concat((batch2['text_embeded'], torch.unsqueeze(batch['text_embeded'][i],0)),0)
            batch2['text'] = torch.concat((batch2['text'], torch.tensor([batch['text'][i]])),0)
            batch2['sound'] = torch.concat((batch2['sound'], torch.tensor([batch['sound'][i]])),0)
            batch2['hashtags_score'] = torch.concat((batch2['hashtags_score'], torch.tensor([batch['hashtags_score'][i]])),0)
            labels2 = torch.concat((labels2,torch.tensor([labels[i]])),0)
    batch1['text'] = batch1['text'][1:]
    batch1['sound'] = batch1['sound'][1:]
    batch1['hashtags_score'] = batch1['hashtags_score'][1:]
    batch2['text'] = batch2['text'][1:]
    batch2['sound'] = batch2['sound'][1:]
    batch2['hashtags_score'] = batch2['hashtags_score'][1:]
    labels1 = labels1[1:]
    labels2 = labels2[1:]
    return [[batch1, labels1], [batch2, labels2]]

def evaluate(testDataLoader, model, loss_function):
    model.eval()
    test_loss = 0
    preds = np.array([])
    reals = np.array([])
    with torch.no_grad():
        for data, target in tqdm(testDataLoader):
            for (data, labels) in split_batch(data, target):
                if len(labels) > 1:
                    output = model(data)
                    test_loss += loss_function(torch.squeeze(output).float(), torch.squeeze(labels).float()).item()

                    preds = np.concatenate((preds, output.detach().flatten()), axis=0)
                    reals = np.concatenate((reals, labels.detach().flatten()), axis=0)

    fpr, tpr, threshold = metrics.roc_curve(reals, preds)
    roc_auc = metrics.auc(fpr, tpr)
    test_loss /= len(testDataLoader.dataset)
    return test_loss, roc_auc, fpr, tpr

def train_epoch(trainDataLoader, model, loss_function, optimizer):
    # model=model.to(device)
    model.train()
    total_loss=0
    preds = np.array([])
    reals = np.array([])
    for (data, target) in tqdm(trainDataLoader):
        for  (data, labels) in split_batch(data, target):
            if len(labels)>1:
                output = model(data)
                loss=loss_function(torch.squeeze(output).float(), torch.squeeze(labels).float())#### handle batch better also avg_loss is incorrect

                preds = np.concatenate((preds, output.detach().flatten()), axis=0)
                reals = np.concatenate((reals, labels.detach().flatten()), axis=0)

                # Update model weights
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                total_loss += loss.item()
    avg_loss = total_loss / len(trainDataLoader.dataset)
    fpr, tpr, threshold = metrics.roc_curve(reals, preds)
    roc_auc = metrics.auc(fpr, tpr)
    return avg_loss, roc_auc


def train_model(model, trainDataLoader, cvDataLoader,  lr=1e-2, epochs = 10):
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    train_loss_list = list()
    train_auc_list = list()
    cv_loss_list = list()
    cv_auc_list = list()
    for epoch in range(epochs):
        print(f'Epoch: {epoch + 1}')
        train_loss, train_auc = train_epoch(trainDataLoader, model, criterion, optimizer)
        train_loss_list.append(train_loss)
        train_auc_list.append(train_auc)
        print(f'train_loss: {train_loss}, train_auc: {train_auc}')
        validation_loss, validation_auc, fpr, tpr = evaluate(cvDataLoader, model, criterion)
        cv_loss_list.append(validation_loss)
        cv_auc_list.append(validation_auc)
        print(f'validation_loss: {validation_loss}, validation_auc: {validation_auc}')

    plt.plot(fpr, tpr,color="darkorange",label="ROC curve (area = %0.2f)" % cv_auc_list[-1])
    plt.show()
    return cv_auc_list[-1]

def get_predict(model, sample):
    model.eval()
    with torch.no_grad():
        return  model(sample)


# if __name__ == "__main__":
#     # vids = np.load('../vids.npy', allow_pickle=True)
#     # tags = np.load('../tag.npy', allow_pickle=True)
#     # data = np.load('../data.npy', allow_pickle=True)
#     # x_train_val, x_test, y_train_val, y_test = train_test_split(data, tags, test_size = 0.15, random_state = 19)
#     # x_train, x_val, y_train, y_val = train_test_split(x_train_val, y_train_val, test_size = 0.15, random_state = 17)
#     # np.save('../data/x_train.npy', x_train)
#     # np.save('../data/y_train.npy', y_train)
#     # np.save('../data/x_val.npy', x_val)
#     # np.save('../data/y_val.npy', y_val)
#     # np.save('../data/x_test.npy', x_test)
#     # np.save('../data/y_test.npy', y_test)
#     ########################################################################################################################3
#     x_train = np.load('../data/x_train.npy', allow_pickle=True)
#     y_train = np.load('../data/y_train.npy', allow_pickle=True)
#     x_val = np.load('../data/x_val.npy', allow_pickle=True)
#     y_val = np.load('../data/y_val.npy', allow_pickle=True)
#     x_test = np.load('../data/x_test.npy', allow_pickle=True)
#     y_test = np.load('../data/y_test.npy', allow_pickle=True)
#     x_train_new = np.load('../data/x_train_new.npy', allow_pickle=True)
#     x_val_new = np.load('../data/x_val_new.npy', allow_pickle=True)
#     x_test_new = np.load('../data/x_test_new.npy', allow_pickle=True)
#     nationalistic_sounds = np.load('../nationalistic_songs.npy', allow_pickle=True)
#     nationalistic_sounds = get_train_sounds.get_train_sounds(x_train, nationalistic_sounds)
#
#     with open("../../../Downloads/train2.txt", "r") as f1:
#         with open("../../../Downloads/trainVecs.json", "r") as f2:
#             videos_id = f1.read().split('\n')[:-1]
#             vectors = json.load(f2)
#     with open("../../../Downloads/val2.txt", "r") as f1:
#         with open("../../../Downloads/testVecs.json", "r") as f2:
#             videos_id += f1.read().split('\n')[:-1]
#             vectors += json.load(f2)
#
#     for i in range(len(videos_id)):
#         videos_id[i] = videos_id[i].split(' ')[0]
#     c = 0
#     i = 0
#     for x in x_train:
#         try:
#             id = x['Vid']
#             x['text_embeded'] = x_train_new[i]['text_embedded'] if x_train_new[i]['text_embedded'] != None else np.random.rand(128)
#             x['text'] = 1 if x_train_new[i]['text_embedded'] != None else 0
#             x['video_vector'] = vectors[videos_id.index(id)]
#         except:
#             x['video_vector'] = x_train[i-1]['video_vector']
#             c+=1
#         i+=1
#     i = 0
#     for x in x_val:
#         try:
#             id = x['Vid']
#             x['text_embeded'] = x_val_new[i]['text_embedded'] if x_val_new[i]['text_embedded'] != None else np.random.rand(128)
#             x['text'] = 1 if x_val_new[i]['text_embedded'] != None else 0
#             x['video_vector'] = vectors[videos_id.index(id)]
#         except:
#             x['video_vector'] = x_val[i-1]['video_vector']
#             c+=1
#         i+=1
#     i = 0
#     for x in x_test:
#         try:
#             id = x['Vid']
#             x['text_embeded'] = x_test_new[i]['text_embedded'] if x_test_new[i]['text_embedded'] != None else np.random.rand( 128)
#             x['text'] = 1 if x_test_new[i]['text_embedded'] != None else 0
#             x['video_vector'] = vectors[videos_id.index(id)]
#         except:
#             x['video_vector'] = x_test[i-1]['video_vector']
#             c+=1
#         i+=1
#     del x_train_new
#     del x_val_new
#     del x_test_new
#
#     # get_hash_score.add_grade(x_train, y_train, x_val, y_val)
#     # get_hash_score.add_grade(x_train, y_train, x_test, y_test)
#     # #
#     # # config = Config()
#     # # nlp_model = nlp.Seq2SeqAttention(config)
#     # # nlp_model.load_state_dict(torch.load('../text_models/text_model.pt', map_location='cpu'))
#     # # dataprep.embed_text(nlp_model, x_train, torch.tensor(np.zeros(len(x_train))))
#     # # dataprep.embed_text(nlp_model, x_val, torch.tensor(np.zeros(len(x_val))))
#     # # dataprep.embed_text(nlp_model, x_test, torch.tensor(np.zeros(len(x_test))))
#     #
#     # train_x = []
#     # val_x = []
#     # test_x = []
#     # for x in x_train:
#     #     sound = 0
#     #     if x['musicId'] in nationalistic_sounds:
#     #         sound = 1
#     #     train_x.append({
#     #         'video_embeded':  torch.tensor(x['video_vector']),
#     #         'hashtags_score': torch.tensor(x['hash_score']),
#     #         'text_embeded':  torch.tensor(x['text_embeded'].reshape(128)),
#     #         'text': torch.tensor(x['text']),
#     #         'sound': torch.tensor([sound])
#     #     })
#     # for x in x_val:
#     #     sound = 0
#     #     if x['musicId'] in nationalistic_sounds:
#     #         sound = 1
#     #     val_x.append({
#     #         'video_embeded':  torch.tensor(x['video_vector']),
#     #         'hashtags_score': torch.tensor(x['hash_score']),
#     #         'text_embeded':  torch.tensor(x['text_embeded'].reshape(128)),
#     #         'text': torch.tensor(x['text']),
#     #         'sound': torch.tensor([sound])
#     #     })
#     # for x in x_test:
#     #     sound = 0
#     #     if x['musicId'] in nationalistic_sounds:
#     #         sound = 1
#     #     test_x.append({
#     #         'video_embeded':  torch.tensor(x['video_vector']),
#     #         'hashtags_score': torch.tensor(x['hash_score']),
#     #         'text_embeded': torch.tensor(x['text_embeded'].reshape(128)),
#     #         'text': torch.tensor(x['text']),
#     #         'sound':  torch.tensor([sound])
#     #     })
#     #
#     # np.save('../data/final_train', train_x)
#     # np.save('../data/final_val', val_x)
#     # np.save('../data/final_test', test_x)
#
#     train_x = np.load('../data/final_train.npy', allow_pickle=True)
#     val_x = np.load('../data/final_val.npy', allow_pickle=True)
#     test_x = np.load('../data/final_test.npy', allow_pickle=True)
#     for x in train_x:
#         # x['text_embeded'] =  torch.tensor(x['text_embeded'].reshape(128))
#         # x['video_embeded'] = torch.tensor(x['video_embeded'])
#         # x['sound']= torch.tensor(x['sound'])
#         x['text'] = torch.tensor(x['text'])
#         # x['hashtags_score'] = torch.tensor(np.random.rand(1))
#         # x['text_embeded'] = torch.tensor(np.random.rand(128))
#         # x['sound'] = torch.tensor(np.random.rand(1))
#         # x['video_embeded'] = torch.tensor(np.random.rand(2048))
#     for x in val_x:
#         # x['text_embeded'] =  torch.tensor(x['text_embeded'].reshape(128))
#         # x['video_embeded'] = torch.tensor( x['video_embeded'])
#         # x['sound']= torch.tensor(x['sound'])
#         x['text'] = torch.tensor(x['text'])
#         # x['hashtags_score'] = torch.tensor(np.random.rand(1))
#         # x['text_embeded'] = torch.tensor(np.random.rand(128))
#         # x['sound'] = torch.tensor(np.random.rand(1))
#         # x['video_embeded'] = torch.tensor(np.random.rand(2048))
#     for x in test_x:
#         # x['text_embeded'] =  torch.tensor(x['text_embeded'].reshape(128))
#         # x['video_embeded'] = torch.tensor( x['video_embeded'])
#         # x['sound']= torch.tensor(x['sound'])
#         x['text'] = torch.tensor(x['text'])
#         # x['hashtags_score'] = torch.tensor(np.random.rand(1))
#         # x['text_embeded'] = torch.tensor(np.random.rand(128))
#         # x['sound'] = torch.tensor(np.random.rand(1))
#         # x['video_embeded'] = torch.tensor(np.random.rand(2048))
#
#
#     train_dataset = postsDataset(train_x, y_train)
#     val_dataset = postsDataset(val_x, y_val)
#     test_dataset = postsDataset(test_x, y_test)
#
#     train_loader = data_utils.DataLoader(dataset = train_dataset, batch_size = 64, shuffle = True)
#     val_loader = data_utils.DataLoader(dataset = val_dataset, batch_size = 32, shuffle = True)
#     test_loader = data_utils.DataLoader(dataset = test_dataset, batch_size = 32, shuffle = True)
#
#     model =  postsModel(dropout_squeeze_fc=0.2, dropout_final_fc=0.2)
#     train_model(model, train_loader, val_loader)
#     model =  postsModel(dropout_squeeze_fc=0.2, dropout_final_fc=0.2)
#     train_model(model, train_loader, test_loader)
#     torch.save(model, 'final_model')


if __name__ == "__main__":
    # x_train = np.load('../data/x_train_new.npy', allow_pickle=True)
    y_train = np.load('../data/y_train.npy', allow_pickle=True)
    # x_test = np.load('../data/x_test_new.npy', allow_pickle=True)
    y_test = np.load('../data/y_test.npy', allow_pickle=True)
    # nationalistic_sounds = np.load('../nationalistic_songs.npy', allow_pickle=True)
    # nationalistic_sounds = get_train_sounds.get_train_sounds(x_train, nationalistic_sounds)
    # with open("../../../Downloads/train2.txt", "r") as f1:
    #     with open("../../../Downloads/trainVecs.json", "r") as f2:
    #         videos_id = f1.read().split('\n')
    #         vectors = json.load(f2)
    # with open("../../../Downloads/test2.txt", "r") as f1:
    #     with open("../../../Downloads/testVecs.json", "r") as f2:
    #         videos_id += f1.read().split('\n')[:-1]
    #         vectors += json.load(f2)
    #
    # for i in range(len(videos_id)):
    #     videos_id[i] = videos_id[i].split(' ')[0]
    # c = 0
    # i = 0
    # for x in x_train:
    #     try:
    #         id = x['Vid']
    #         x['text_embeded'] = x_train[i]['text_embeded'] if x_train[i]['text'] != 0 else np.random.rand(128)
    #         x['video_vector'] = vectors[videos_id.index(id)]
    #     except:
    #         x['video_vector'] = x_train[i-1]['video_vector']
    #         c+=1
    #     i+=1
    # i = 0
    # for x in x_test:
    #     try:
    #         id = x['Vid']
    #         x['text_embeded'] = x_test[i]['text_embeded'] if x_test[i]['text'] != 0 else np.random.rand(128)
    #         x['video_vector'] = vectors[videos_id.index(id)]
    #     except:
    #         x['video_vector'] = x_test[i - 1]['video_vector']
    #         c += 1
    #     i += 1
    #
    # train_x = []
    # test_x = []
    # for x in x_train:
    #     sound = 0
    #     if x['musicId'] in nationalistic_sounds:
    #         sound = 1
    #     train_x.append({
    #         'video_embeded':  torch.tensor(np.array(x['video_vector'])[:,0]),
    #         'hashtags_score': torch.tensor(x['hash_score']),
    #         'text_embeded':  torch.tensor(x['text_embeded']).reshape(-1),
    #         'text': torch.tensor(x['text']),
    #         'sound': torch.tensor([sound])
    #     })
    # for x in x_test:
    #     sound = 0
    #     if x['musicId'] in nationalistic_sounds:
    #         sound = 1
    #     test_x.append({
    #         'video_embeded':   torch.tensor(np.array(x['video_vector'])[:,0]),
    #         'hashtags_score': torch.tensor(x['hash_score']),
    #         'text_embeded': torch.tensor(x['text_embeded']).reshape(-1),
    #         'text': torch.tensor(x['text']),
    #         'sound':  torch.tensor([sound])
    #     })
    #
    # np.save('../data/final_train', train_x)
    # np.save('../data/final_test', test_x)

    train_x = np.load('../data/final_train.npy', allow_pickle=True)
    test_x = np.load('../data/final_test.npy', allow_pickle=True)

    # for x in train_x:
        # x['hashtags_score'] = torch.tensor(np.random.rand(1))
        # x['text_embeded'] = torch.tensor(np.random.rand(128))
        # x['sound'] = torch.tensor(np.random.rand(1))
        # x['video_embeded'] = torch.tensor(np.random.rand(30))

    train_dataset = postsDataset(train_x, y_train)
    test_dataset = postsDataset(test_x, y_test)

    train_loader = data_utils.DataLoader(dataset = train_dataset, batch_size = 64, shuffle = True)
    test_loader = data_utils.DataLoader(dataset = test_dataset, batch_size = 32, shuffle = True)

    model =  postsModel(dropout_squeeze_fc=0.3, dropout_final_fc=0.3)
    train_model(model, train_loader, test_loader)
    torch.save(model, 'final_model')