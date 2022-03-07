import random
import pymongo as pymongo
import torch
import pandas as pd
import torch.nn.functional as F
import numpy as np
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
import pymongo
import os
import torchvision
from PIL import Image
import torch.utils.data as data_utils
import cv2
from sklearn.model_selection import train_test_split
from sklearn import metrics
from torchvision import datasets, models, transforms

EPOCHS = 50
OUT_CHANNELS_INITIAL = 10
INITIAL_KERNEL_SIZE = 3
CNN_STRIDE = 1
POOLING_KERNEL_SIZE = 2
POOLING_STRIDE = 2
CONV_SIZE_1 = 16
FC_SIZE = 64
CNN_DROPOUTDROPOUT = 0.1
CONV_LAYER_DROPOUT = 0.1

class resnet(nn.Module):
    def __init__(self, layers_to_freeze):
        super().__init__()
        self.model_conv = torchvision.models.resnet18(pretrained=True)
        i = 0
        for param in self.model_conv.parameters():
            if i < layers_to_freeze:
                param.requires_grad = False
            i+=1

        # Parameters of newly constructed modules have requires_grad=True by default
        self.num_ftrs = self.model_conv.fc.in_features
        self.model_conv.fc = nn.Linear(self.num_ftrs, 1)

    def forward(self, x):
        return torch.sigmoid(self.model_conv(x))


class ConvolutionLayer(nn.Module):
    def __init__(self, input_channels, output_channels1, output_channels2):
        super().__init__()
        self.convolution1 = nn.Conv2d(input_channels, output_channels1, kernel_size=3, stride=1)
        self.batch_norm1 = nn.BatchNorm2d(output_channels1)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=CONV_LAYER_DROPOUT)
        self.convolution2 = nn.Conv2d(output_channels1, output_channels2, kernel_size=3, stride=1)
        self.batch_norm2 = nn.BatchNorm2d(output_channels2)

    def forward(self, x):
        output = self.convolution1(x)
        output = self.batch_norm1(output)
        output = self.relu(output)
        output = self.dropout(output)
        output = self.convolution2(output)
        output = self.batch_norm2(output)
        output = self.relu(output)
        return output


class CNN(nn.Module):
    def __init__(self, ):
        super().__init__()
        self.convolution = nn.Conv2d(3, OUT_CHANNELS_INITIAL, kernel_size=INITIAL_KERNEL_SIZE,
                                     stride=1)
        self.input_channels = OUT_CHANNELS_INITIAL
        self.relu = nn.ReLU()
        self.batch_norm1 = nn.BatchNorm2d(OUT_CHANNELS_INITIAL)
        self.layer1 = self.add_convolutiona_layer(CONV_SIZE_1, CONV_SIZE_1)
        self.pooling = nn.MaxPool2d(kernel_size=POOLING_KERNEL_SIZE, stride=POOLING_STRIDE)

        self.fc_1 = nn.Linear(500544, FC_SIZE)
        self.batch_norm2 = nn.BatchNorm1d(FC_SIZE)
        self.fc_2 = nn.Linear(FC_SIZE, 1)
        self.dropout = nn.Dropout(p=CNN_DROPOUTDROPOUT)

    def add_convolutiona_layer(self, output_channels1, output_channels2):
        layer = ConvolutionLayer(self.input_channels, output_channels1, output_channels2)
        self.input_channels = output_channels2
        return layer

    def forward(self, x):
        out = self.convolution(x)
        out = self.batch_norm1(out)
        out = self.pooling(out)
        out = self.layer1(out)
        out = self.pooling(out)
        out = out.view(out.size(0), -1)
        out = self.dropout(out)
        out = self.fc_1(out)
        out = self.batch_norm2(out)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.fc_2(out)
        return F.sigmoid(out)

def get_data():
    # myclient = pymongo.MongoClient("mongodb+srv://ourProject:EMGwk59xADuSIIkv@cluster0.lhfaj.mongodb.net/production2?retryWrites=true&w=majority")
    # db = myclient['production2']
    # tags = db['israeltags']
    # tagged_videos = []
    # videos = []
    #
    # # get tags of images
    # for file in os.listdir('images/'):
    #     fileName=file.split(".")[0]
    #     tag = tags.find_one({'id':  fileName})
    #     try:
    #         if tag['tagged']:
    #             tagged_videos.append((fileName, tag['decision']))
    #     except:
    #         pass
    #
    # sizes = [[], []]
    # minsizes = [np.inf, np.inf]
    # for im in tagged_videos:
    #     img = Image.open('images/'+ im[0] +'.png').convert('RGBA')
    #     arr = np.array(img)[:,:,:-1]
    #     sizes[0].append(arr.shape[0])
    #     sizes[1].append(arr.shape[1])
    # avg = [np.average(np.array(sizes[0])), np.average(np.array(sizes[1]))]
    # std = [np.std(np.array(sizes[0])), np.std(np.array(sizes[1]))]
    # tags = []
    # for im in tagged_videos:
    #     img = Image.open('images/'+ im[0] +'.png').convert('RGBA')
    #     arr = np.array(img)[:,:,:-1]
    #     if arr.shape[0] > avg[0] - 3 * std[0] and  arr.shape[1] > avg[1] - 3 * std[1] and arr.shape[0] < avg[0] + 3 * std[0] and arr.shape[1] < avg[1] + 3 * std[1]:
    #         videos.append(arr)
    #         tags.append(1 if im[1] else 0)
    #         if arr.shape[0] < minsizes[0]:
    #             minsizes[0] = arr.shape[0]
    #         if arr.shape[1] < minsizes[1]:
    #             minsizes[1] = arr.shape[1]
    #
    # np.save('tagged_images.npy', videos)
    # np.save('images_tags.npy', tags)

    videos = np.load('tagged_images.npy', allow_pickle=True)[:1000]
    tags = np.load('images_tags.npy', allow_pickle=True)[:1000]

    minsizes = [960, 540]
    for i in range(len(videos)):
        videos[i] = cv2.resize(videos[i], dsize=(minsizes[0], minsizes[1]), interpolation=cv2.INTER_CUBIC)
        videos[i] = videos[i].reshape(3, minsizes[0], minsizes[1]) # am I doing it right????????????????????????????????
        videos[i] = videos[i].astype(float)
        videos[i] /= 255
        videos[i] = list(videos[i])
    videos = videos.tolist()
    videos=np.array(videos).astype(float)
    np.save('tagged_images.npy', videos)
    np.save('images_tags.npy', tags)
    videos = np.load('tagged_images.npy', allow_pickle=True)
    tags = np.load('images_tags.npy', allow_pickle=True)


    x_train, x_test, y_train, y_test = train_test_split(videos, tags, test_size=0.2, shuffle=True)
    x_train = torch.tensor(x_train)
    x_test = torch.tensor(x_test)
    y_train = torch.tensor(y_train)
    y_test = torch.tensor(y_test)
    train_tensor = data_utils.TensorDataset(x_train, y_train)
    test_tensor = data_utils.TensorDataset(x_test, y_test)
    train_loader = data_utils.DataLoader(dataset=train_tensor, batch_size=32, shuffle=True)
    test_loader = data_utils.DataLoader(dataset=test_tensor, batch_size=32, shuffle=False)
    return  train_loader, test_loader

def train_epoch(train_loader, model, optimizer):
    model.train()
    total_loss = 0
    preds = np.array([])
    reals = np.array([])
    loss_func = nn.BCELoss()

    for input, labels in tqdm(train_loader):
        input = input.cuda()
        labels = labels.cuda()
        input = input.cuda()
        labels = labels.cuda()
        outputs = model(input.float())
        outputs = outputs.squeeze()
        preds = np.concatenate((preds, outputs.detach().flatten()), axis=0)
        reals = np.concatenate((reals, labels.detach().flatten()), axis=0)

        # Compute loss
        loss = loss_func(outputs, labels.float())

        # Update model weights
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
    fpr, tpr, threshold = metrics.roc_curve(reals, preds)
    roc_auc = metrics.auc(fpr, tpr)
    # Return average loss
    return total_loss/ len(train_loader), roc_auc

def eval(model, data_loader):
    model.eval()
    test_loss = 0
    preds = np.array([])
    reals = np.array([])
    loss_func = nn.BCELoss()

    with torch.no_grad():
        for data, target in data_loader:
            data = data.cuda()
            target = target.cuda()
            data = data.float()
            target = target.float()
            output = model(data)
            output = output.squeeze()
            test_loss += loss_func(output, target)
            preds = np.concatenate((preds, output.detach().flatten()), axis=0)
            reals = np.concatenate((reals, target.detach().flatten()), axis=0)

    fpr, tpr, threshold = metrics.roc_curve(reals, preds)
    roc_auc = metrics.auc(fpr, tpr)
    return test_loss/ len(data_loader), roc_auc


def train_model(train_loader, validation_loader):
    model = resnet(0)
    optimizer = optim.Adam(model.parameters(), lr=1e-2)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device)
    train_loss_list = list()
    train_auc_list = list()
    validation_loss_list = list()
    validation_auc_list = list()

    for epoch in range(EPOCHS):
        print(f'Epoch: {epoch + 1} / {EPOCHS}')
        train_loss, train_auc = train_epoch(train_loader, model, optimizer)
        print("train loss:" + str(train_loss))
        print("train acc:" + str(train_auc))
        train_loss_list.append(train_loss)
        train_auc_list.append(train_auc)
        val_loss, val_auc = eval(model, validation_loader)
        print("val loss:" + str(val_loss))
        print("val acc:" + str(val_auc))
        validation_loss_list.append(val_loss)
        validation_auc_list.append(val_auc)
    return model

if __name__ == "__main__":
    train_loader, test_loader = get_data()
    train_model(train_loader, test_loader)
