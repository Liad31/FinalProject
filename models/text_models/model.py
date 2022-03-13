# model.py

import torch
from torch import nn
import numpy as np
from torch.nn import functional as F
from sklearn.metrics import accuracy_score, log_loss, auc, roc_curve


# from utils import *


class Seq2SeqAttention(nn.Module):
    def __init__(self, config):
        super(Seq2SeqAttention, self).__init__()
        self.config = config

        # Encoder RNN
        self.lstm = nn.LSTM(input_size=self.config.embed_size,
                            hidden_size=self.config.hidden_size,
                            num_layers=self.config.hidden_layers,
                            bidirectional=self.config.bidirectional)

        # Dropout Layer
        self.dropout = nn.Dropout(self.config.dropout_keep)

        # Fully-Connected Layer
        self.fc = nn.Linear(
            self.config.hidden_size * (1 + self.config.bidirectional) * 2,
            1
        )

        # Softmax non-linearity
        self.softmax = nn.Sigmoid()

    def apply_attention(self, rnn_output, final_hidden_state):
        '''
        Apply Attention on RNN output

        Input:
            rnn_output (batch_size, seq_len, num_directions * hidden_size): tensor representing hidden state for every word in the sentence
            final_hidden_state (batch_size, num_directions * hidden_size): final hidden state of the RNN

        Returns:
            attention_output(batch_size, num_directions * hidden_size): attention output vector for the batch
        '''
        hidden_state = final_hidden_state.unsqueeze(2)
        attention_scores = torch.bmm(rnn_output, hidden_state).squeeze(2)
        soft_attention_weights = F.softmax(attention_scores, 1).unsqueeze(2)  # shape = (batch_size, seq_len, 1)
        attention_output = torch.bmm(rnn_output.permute(0, 2, 1), soft_attention_weights).squeeze(2)
        return attention_output

    def forward(self, x):
        # x.shape = (max_sen_len, batch_size)
        # embedded_sent.shape = (max_sen_len=20, batch_size=64,embed_size=300)

        ##################################### Encoder #######################################
        lstm_output, (h_n, c_n) = self.lstm(x)
        # lstm_output.shape = (seq_len, batch_size, num_directions * hidden_size)

        # Final hidden state of last layer (num_directions, batch_size, hidden_size)
        batch_size = h_n.shape[1]
        h_n_final_layer = h_n.view(self.config.hidden_layers,
                                   self.config.bidirectional + 1,
                                   batch_size,
                                   self.config.hidden_size)[-1, :, :, :]

        ##################################### Attention #####################################
        # Convert input to (batch_size, num_directions * hidden_size) for attention
        final_hidden_state = torch.cat([h_n_final_layer[i, :, :] for i in range(h_n_final_layer.shape[0])], dim=1)

        attention_out = self.apply_attention(lstm_output.permute(1, 0, 2), final_hidden_state)
        # Attention_out.shape = (batch_size, num_directions * hidden_size)

        #################################### Linear #########################################
        concatenated_vector = torch.cat([final_hidden_state, attention_out], dim=1)
        final_feature_map = self.dropout(concatenated_vector)  # shape=(batch_size, num_directions * hidden_size)
        final_out = self.fc(final_feature_map)
        return self.softmax(final_out)

    def forward_to_last_layer(self, x):
        # x.shape = (max_sen_len, batch_size)
        # embedded_sent.shape = (max_sen_len=20, batch_size=64,embed_size=300)

        ##################################### Encoder #######################################
        lstm_output, (h_n, c_n) = self.lstm(x)
        # lstm_output.shape = (seq_len, batch_size, num_directions * hidden_size)

        # Final hidden state of last layer (num_directions, batch_size, hidden_size)
        batch_size = h_n.shape[1]
        h_n_final_layer = h_n.view(self.config.hidden_layers,
                                   self.config.bidirectional + 1,
                                   batch_size,
                                   self.config.hidden_size)[-1, :, :, :]

        ##################################### Attention #####################################
        # Convert input to (batch_size, num_directions * hidden_size) for attention
        final_hidden_state = torch.cat([h_n_final_layer[i, :, :] for i in range(h_n_final_layer.shape[0])], dim=1)

        attention_out = self.apply_attention(lstm_output.permute(1, 0, 2), final_hidden_state)
        # Attention_out.shape = (batch_size, num_directions * hidden_size)

        #################################### Linear #########################################
        concatenated_vector = torch.cat([final_hidden_state, attention_out], dim=1)
        final_feature_map = self.dropout(concatenated_vector)  # shape=(batch_size, num_directions * hidden_size)
        return final_feature_map

    def add_optimizer(self, optimizer):
        self.optimizer = optimizer

    def add_loss_op(self, loss_op):
        self.loss_op = loss_op

    def reduce_lr(self):
        print("Reducing LR")
        for g in self.optimizer.param_groups:
            g['lr'] = g['lr'] / 2

    def run_epoch(self, train_iterator, val_iterator, epoch):
        for i, batch in enumerate(train_iterator):
            self.optimizer.zero_grad()
            if torch.cuda.is_available():
                x = batch[0].cuda()
                y = (batch[1]).type(torch.cuda.FloatTensor)
            else:
                x = batch[0]
                y = (batch[1]).type(torch.FloatTensor)
            y_pred = self.__call__(x)
            loss = self.loss_op(y_pred, y)
            loss.backward()
            self.optimizer.step()

    def evaluate_model(self, iterator):
        all_preds = []
        all_y = []
        losses = []
        for idx, batch in enumerate(iterator):
            if torch.cuda.is_available():
                x = batch[0].cuda()
            else:
                x = batch[0]
            y_pred = self(x)
            predicted = self(x) > 0.5
            # predicted = torch.max(y_pred.cpu().data, 1)[1]
            loss = self.loss_op(y_pred.cpu(), batch[1].type(torch.FloatTensor))
            losses.append(loss.data.cpu().numpy())
            all_preds.extend(predicted.cpu().numpy())
            all_y.extend(batch[1].numpy())
        score = accuracy_score(all_y, np.array(all_preds).flatten())
        loss = np.mean(losses)
        return score, loss

    def evaluate_auc(self, iterator):
        all_preds = []
        all_y = []
        for batch in iterator:
            if torch.cuda.is_available():
                x = batch[0].cuda()
            else:
                x = batch[0]
            y_pred = self(x)
            all_preds.extend(y_pred.cpu().detach().numpy())
            all_y.extend(batch[1].numpy())
        fpr, tpr, thresholds = roc_curve(all_y, np.array(all_preds).flatten(), pos_label=1)
        return auc(fpr, tpr)

