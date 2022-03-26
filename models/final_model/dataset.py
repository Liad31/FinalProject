import os
import torch
import pandas as pd
from skimage import io, transform
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils

class postsDataset(Dataset):

    def __init__(self, posts_data, tags):
        if len(tags) != len(posts_data):
            exit(-1)
        self.posts = posts_data
        self.tags = tags

    def __len__(self):
        return len(self.tags)

    def __getitem__(self, idx):
        return  self.posts[idx], self.tags[idx]