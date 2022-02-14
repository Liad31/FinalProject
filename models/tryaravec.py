import gensim
import re
import numpy as np
import torch
from nltk import ngrams
from model import *
from dataprep import *
from config import Config
import random
import matplotlib.pyplot as plt
from early_stopping import EarlyStopping


# t_model = gensim.models.Word2Vec.load('full_uni_sg_100_twitter.mdl')
# word_vectors = t_model.wv
# del t_model
# key = 'سلاام'
# print(key in word_vectors)
# vector = word_vectors[key]
# print(vector)

# print(word_vectors['ناقص']) # חסר


# sen = [("البتاع والتبديع", 1), ("أحمد فؤاد الرأسمال الثقافي", 1), ("عيش البورجوازية عيش قلق", 0),
#        ("تتفجّر فيه الفتن الفورات", 1), ("نجم البلاغة", 0)]
# train_df = []
# for (se, tag) in sen:
#     se = clean_str(se)
#     # print(se)
#     se = se.split(' ')
#     se = [word_vectors[word] for word in se]
#     train_df.append((se, tag))
#
# train_df = np.array(train_df, dtype=object)
# train_tmp = split_to_batches(train_df, 2)

data = load_my_data()
random.shuffle(data)
train_size = int(0.8*len(data))
train_set, val_set = torch.utils.data.random_split(data, [train_size, len(data) - train_size])
train_iter = split_to_batches(train_set, 4)
val_iter = split_to_batches(val_set, 4)

config = Config()
model = Seq2SeqAttention(config)
loss = torch.nn.BCELoss()
if torch.cuda.is_available():
    model.cuda()
    loss.cuda()
model.add_optimizer(torch.optim.Adam(model.parameters()))
model.add_loss_op(loss)

stopper = EarlyStopping(patience=10)
train_losses = []
train_accuracies = []
val_losses = []
val_accuracies = []
epoch = 0
for epoch in range(100):
    random.shuffle(train_iter)
    random.shuffle(val_iter)
    model.train()
    model.run_epoch(train_iter, val_iter, epoch)
    model.eval()
    train_acc, train_loss = model.evaluate_model(train_iter)
    val_acc, val_loss = model.evaluate_model(val_iter)
    train_losses.append(train_loss)
    train_accuracies.append(train_acc)
    val_losses.append(val_loss)
    val_accuracies.append(val_acc)
    print("Epoch: {}".format(epoch))
    print("\tAverage training loss: {:.7f}".format(train_loss))
    print("\tTrain Accuracy: {:.7f}".format(train_acc))
    print("\tAverage val loss: {:.7f}".format(val_loss))
    print("\tVal Accuracy: {:.4f}".format(val_acc))
    stopper(val_loss, model)
    if stopper.early_stop:
        break


# for graphs
# Initialise the subplot
figure, axis = plt.subplots(2, 2)
X = [i for i in range(epoch + 1)]
figure.suptitle('My Model', fontsize=16)

# For valid loss Function
axis[0, 0].plot(X, val_losses)
axis[0, 0].set_title("loss on validation set")
axis[0, 0].set_xlabel("Epoch Number")
axis[0, 0].set_ylabel("loss")

# For train loss Function
axis[0, 1].plot(X, train_losses)
axis[0, 1].set_title("loss on training set")
axis[0, 1].set_xlabel("Epoch Number")
axis[0, 1].set_ylabel("loss")

# For valid accur Function
axis[1, 0].plot(X, val_accuracies)
axis[1, 0].set_title("accuracy on validation set")
axis[1, 0].set_xlabel("Epoch Number")
axis[1, 0].set_ylabel("accuracy")

# For train accure Function
axis[1, 1].plot(X, train_accuracies)
axis[1, 1].set_title("accuracy on training set")
axis[1, 1].set_xlabel("Epoch Number")
axis[1, 1].set_ylabel("accuracy")

# display
plt.show()


