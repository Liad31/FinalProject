import math
import os
import random
from collections import defaultdict
import torch.utils.data as data_utils
from sklearn.model_selection import train_test_split
import cv2
from tqdm import tqdm
import pandas as pd
import numpy as np
import torch
from scikitplot import metrics
from torch import nn, optim
from torch.utils.data import Dataset
from skimage.transform import resize
import ffmpeg
import cv2
from torchvision import models
from moviepy.editor import VideoFileClip
EPOCHS = 100


class VideoDataset(Dataset):
    """Video dataset."""

    def __init__(self, datas, timesep=75, rgb=3, h=288, w=512):
        """
        Args:
            datas: pandas dataframe contain path to videos files with label of them
            timesep: number of frames
            rgb: number of color channels
            h: height
            w: width

        """
        self.dataloctions = datas
        self.timesep, self.rgb, self.h, self.w = timesep, rgb, h, w

    def __len__(self):
        return len(self.dataloctions)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        video = capture(self.dataloctions.iloc[idx, 0], int(self.timesep * self.dataloctions.iloc[idx, 2]), self.rgb, self.h, self.w)
        sample = {'video': torch.from_numpy(video),
                  'label': torch.from_numpy(np.asarray(self.dataloctions.iloc[idx, 1]))}

        return sample

def lengths_clones(samples):
    d = defaultdict(list)
    for s in samples.index:
        d[samples.loc[s,:].iat[2]].append(samples.loc[s,:])
    result = []
    for n in sorted(d, reverse=True):
        if n > 0:
            clone = d[n]
            clone = np.array(clone)
            result.append(
                clone)

    return result

def split_to_batches(samples, batch_size):
    batches = list()
    batch =  [samples[i:i+batch_size,:] for i in range(0, int(math.ceil(samples.shape[0]/batch_size)))]
    for j in range(len(batch)):
        batches.append(batch[j])
    return batches

def capture(filename, timesep, rgb, h, w):
    tmp = []
    frames = np.zeros((timesep, rgb, h, w), dtype=np.float)
    i = 0
    vc = cv2.VideoCapture(filename)
    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False
    frm = resize(frame, (h, w, rgb))
    frm = np.expand_dims(frm, axis=0)
    frm = np.moveaxis(frm, -1, 1)
    if (np.max(frm) > 1):
        frm = frm / 255.0
    frames[i][:] = frm
    i += 1
    while i < timesep:
        tmp[:] = frm[:]
        rval, frame = vc.read()
        frm = resize(frame, (h, w, rgb))
        frm = np.expand_dims(frm, axis=0)
        if (np.max(frm) > 1):
            frm = frm / 255.0
        frm = np.moveaxis(frm, -1, 1)
        frames[i - 1][:] = frm  # - tmp
        i += 1

    return frames

class TimeWarp(nn.Module):
    def __init__(self, baseModel, method='sqeeze'):
        super(TimeWarp, self).__init__()
        self.baseModel = baseModel
        self.method = method

    def forward(self, x):
        batch_size, time_steps, C, H, W = x.size()
        if self.method == 'loop':
            output = []
            for i in range(time_steps):
                # input one frame at a time into the basemodel
                x_t = self.baseModel(x[:, i, :, :, :])
                # Flatten the output
                x_t = x_t.view(x_t.size(0), -1)
                output.append(x_t)
            # end loop
            # make output as  ( samples, timesteps, output_size)
            x = torch.stack(output, dim=0).transpose_(0, 1)
            output = None  # clear var to reduce data  in memory
            x_t = None  # clear var to reduce data  in memory
        else:
            # reshape input  to be (batch_size * timesteps, input_size)
            x = x.contiguous().view(batch_size * time_steps, C, H, W)
            x = self.baseModel(x)
            x = x.view(x.size(0), -1)
            # make output as  ( samples, timesteps, output_size)
            x = x.contiguous().view(batch_size, time_steps, x.size(-1))
        return x

class extractlastcell(nn.Module):
    def forward(self, x):
        out, _ = x
        return out[:, -1, :]

class videoFightModel(nn.Module):
    def __init__(self,hidden_size=80, dropout=0.2,num_of_layers=1, layers_to_freeze=22, fc_size=256, wight='Statemamonmixed96accviolance.pth'):
        # Create model
        super().__init__()
        pretrained = True
        self.baseModel = models.vgg19(pretrained=pretrained).features
        i = 0
        for child in self.baseModel.children():
            if i < layers_to_freeze:
                for param in child.parameters():
                    param.requires_grad = False
            else:
                for param in child.parameters():
                    param.requires_grad = True
            i +=1

        num_features = 92160 # 12800 in 170
        self.sequential1 = nn.Sequential(TimeWarp(self.baseModel,method='loop'))
        self.sequential12 = nn.Sequential(nn.LSTM(num_features, hidden_size, num_of_layers , batch_first=True , bidirectional=True ),
                            extractlastcell(),
                            nn.Linear(hidden_size*2, fc_size),
                            nn.ReLU(),
                            nn.Dropout(dropout),
                            nn.Linear(fc_size, 1),
                            nn.Sigmoid())

        checkpoint = torch.load(wight, map_location='cpu')
        i = 0
        keys_to_drop = []
        for key, value in checkpoint['state_dict'].items():
            if i > 31:
                keys_to_drop.append(key)
            i+=1
        for key in keys_to_drop:
            checkpoint['state_dict'].pop(key)
        self.sequential1.load_state_dict(checkpoint['state_dict'])

    def forward(self, x):
        x = self.sequential1(x)
        return self.sequential12(x)

def train_epoch(train_batches, model, optimizer, loss_func, train_size):
    model.train()
    total_loss = 0
    preds = np.array([])
    reals = np.array([])

    for i in tqdm(range(len(train_batches))):
        train_dataset = VideoDataset(pd.DataFrame(train_batches[i]))
        train_loader = data_utils.DataLoader(dataset=train_dataset, batch_size=len(train_batches[i]), shuffle=True)
        for sample in train_loader: # only one sample of course
            input = sample['video']
            labels = sample['label']
            input = input.float()
            labels = labels.to(torch.float32)
            outputs = model(input).squeeze()
            preds = np.concatenate((preds, outputs.detach().flatten()), axis=0)
            reals = np.concatenate((reals, labels.detach().flatten()), axis=0)

            # Compute loss
            loss = loss_func(outputs, labels)

            # Update model weights
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
    fpr, tpr, threshold = metrics.roc_curve(reals, preds)
    roc_auc = metrics.auc(fpr, tpr)
    # Return average loss
    return total_loss/ train_size, roc_auc

def eval(model, test_batches, loss_func, test_size):
    model.eval()
    test_loss = 0
    preds = np.array([])
    reals = np.array([])
    with torch.no_grad():
        for i in tqdm(range(len(test_batches))):
            test_dataset = VideoDataset(pd.DataFrame(test_batches[i]))
            test_loader = data_utils.DataLoader(dataset=test_dataset, batch_size=len(test_batches[i]), shuffle=True)
            for sample in test_loader:  # only one sample of course
                input = sample['video']
                labels = sample['label']
                input = input.float()
                labels = labels.to(torch.float32)
                output = model(input)
                test_loss += loss_func(output, labels)
                preds = np.concatenate((preds, output.detach().flatten()), axis=0)
                reals = np.concatenate((reals, labels.detach().flatten()), axis=0)

    fpr, tpr, threshold = metrics.roc_curve(reals, preds)
    roc_auc = metrics.auc(fpr, tpr)
    return test_loss/ test_size, roc_auc


def train_model(df):
    model = videoFightModel()
    optimizer = optim.Adam(model.parameters(), lr=1e-2)
    loss_func = nn.BCELoss()
    train_loss_list = list()
    train_auc_list = list()
    validation_loss_list = list()
    validation_auc_list = list()
    train_df, test_df = train_test_split(df, test_size=0.2, shuffle=True)
    train, test = lengths_clones(train_df), lengths_clones(test_df)

    for epoch in range(EPOCHS):
        print(f'Epoch: {epoch + 1} / {EPOCHS}')
        train_batches = []
        test_batches = []
        for size in train:
            np.random.shuffle(size)
            train_tmp = split_to_batches(size, 2)
            train_batches += train_tmp
        for size in test:
            np.random.shuffle(size)
            test_tmp = split_to_batches(size, 2)
            test_batches += test_tmp
        np.random.shuffle(train_batches)
        np.random.shuffle(test_batches)


        train_loss, train_auc = train_epoch(train_batches, model, optimizer, loss_func, train_size=0.8 * df.shape[0])
        print("train loss:" + str(train_loss))
        print("train acc:" + str(train_auc))
        train_loss_list.append(train_loss)
        train_auc_list.append(train_auc)
        val_loss, val_auc = eval(model, test_batches, loss_func, test_size=0.2 * df.shape[0])
        print("val loss:" + str(val_loss))
        print("val acc:" + str(val_auc))
        validation_loss_list.append(val_loss)
        validation_auc_list.append(val_auc)
    return model

if __name__ == "__main__":
    command_path = './commands'
    dir = '/mnt/tmp/videos'
    outputDir= 'resized'
    widths= []
    heights = []
    resizeBatchSize= 100
    files=os.listdir(dir)
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    for i in range(0,len(files),resizeBatchSize):
        if os.path.exists(command_path):
            os.remove(command_path)
        for vid_path in files[i:i+resizeBatchSize]:
            if vid_path.endswith(".mp4"):
                if "_r" in vid_path:
                    continue
                vid_path = dir + '/' + os.fsdecode(vid_path)
                vcap = cv2.VideoCapture(vid_path)  # 0=camera
                if vcap.isOpened():
                    # get vcap property
                    width = vcap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float `width`
                    height = vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # flo
                    bitrate= vcap.get(cv2.CAP_PROP_BITRATE)
                    newBitrate= min(max(bitrate/2,200),900)
                    newBitrate= int(newBitrate)
                # os.system(f"cp {vid_path} .")
                command = f"ffmpeg -i {vid_path} -s {512}x{288} -b:v {newBitrate}k -map 0:v {outputDir}/{vid_path.split('/')[-1]}"
                os.system(f"echo {command} >> {command_path}")
        os.system(f"parallel -a {command_path}")


    # dir = 'Data/resized/'
    # df = pd.DataFrame(['0', 0]).T
    # for vid_path in os.listdir(dir):
    #     vid_path = dir + vid_path
    #     clip = VideoFileClip(vid_path)
    #     df = df.append({0: vid_path, 1: random.randint(0,1), 2: int(clip.duration/15) if int(clip.duration/15) < 14 else 13},  ignore_index = True)
    # df = df.iloc[1:,:]

    # train_model(df)