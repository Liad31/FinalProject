# config.py

class Config(object):
    def __init__(self):
        self.embed_size = 300
        self.hidden_layers = 1
        self.hidden_size = 32
        self.bidirectional = True
        # self.output_size = 1
        # self.max_epochs = 15
        self.lr = 0.0001
        self.batch_size = 8
        self.dropout_keep = 0.5
        self.patience = 5
        # self.max_sen_len = 30 # Sequence length for RNN

    def set(self, params):
        self.embed_size = params['embed_size']
        self.hidden_layers = params['hidden_layers_lstm']
        self.hidden_size = params['hidden_size_lstm']
        self.bidirectional = params['bidirectional']
        self.lr = params['lr']
        self.batch_size = params['batch_size']
        self.dropout_keep = params['dropout_keep']
        self.patience = params['patience']
