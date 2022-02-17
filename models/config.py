# config.py

class Config(object):
    embed_size = 100
    hidden_layers = 2
    hidden_size = 32
    bidirectional = True
    # output_size = 1
    # max_epochs = 15
    lr = 0.0001
    batch_size = 8
    dropout_keep = 0.5
    # max_sen_len = 30 # Sequence length for RNN

    def set(self, params):
        embed_size = params['embed_size']
        hidden_layers = params['hidden_layers']
        hidden_size = params['hidden_size']
        bidirectional = params['bidirectional']
        lr = params['lr']
        batch_size = params['batch_size']
        dropout_keep = params['dropout_keep']